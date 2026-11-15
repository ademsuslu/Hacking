# ssh for windows

## SSH for Windows: `plink.exe`

**Getting To Know Plink**

![plink-exe](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/66-1.png)



### Using `Plink.exe`

**A-B-C Mantığıyla:**
*   **A (Windows Attack Host):** `plink` komutunu çalıştıran makine.
*   **B (Ubuntu Pivot):** `10.129.15.50` (Tünelin geçtiği makine).
*   **C (Windows Hedefi):** `172.16.5.19` (Ulaşmak istediğin hedef).

```cmd
# windowsda
# username@ip b-makinaına ait
plink -ssh -D 9050 ubuntu@10.129.15.50
```


## proxyfier

Proxifier adlı bir diğer Windows tabanlı araç, oluşturduğumuz `SSH` oturumu üzerinden bir `SOCKS` tüneli başlatmak için kullanılabilir. 


![proxy-fier](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/reverse_shell_9.png)


# Port Forwarding with Windows Netsh


B (Pivot) makinesi bir **Windows** makinesi olduğu için, SSH veya Socat yerine Windows'un kendi yerleşik aracı olan **`netsh`** kullanıyoruz. 

Yine A-B-C mantığıyla hem özetini hem de not alacağın kodları vereyim:

**Makineler:**
*   **A (Saldırgan):** Senin makinen (10.10.15.5)
*   **B (Pivot/Windows 10):** Ele geçirdiğin aracı makine (Dış: 10.129.15.150, İç: 172.16.5.19)
*   **C (Hedef/Windows Server):** İç ağdaki asıl sunucu (172.16.5.25 - RDP Portu: 3389)

**Amaç:** Sen (A), C makinesine RDP (3389) ile bağlanmak istiyorsun ama doğrudan göremiyorsun. B makinesini (Windows) köprü yapacaksın.

### Not Alacağın Kodlar ve Anlamları:

**1. Adım: Port Yönlendirmeyi Kur (B Makinesinde)**
B makinesinde (Windows CMD) şu komutu çalıştırıyorsun:
```cmd
netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=10.129.15.150 connectport=3389 connectaddress=172.16.5.25
```
*   **`listenport=8080` / `listenaddress=10.129.15.150`:** B makinesinin dış IP'sinde (senin erişebildiğin IP) 8080 portunu dinlemeye başla.
*   **`connectport=3389` / `connectaddress=172.16.5.25`:** Buraya gelen trafiği, C makinesinin (Windows Server) 3389 (RDP) portuna gönder.

**2. Adım: Kuralın Eklendiğini Doğrula (B Makinesinde)**
```cmd
netsh.exe interface portproxy show v4tov4
```
*(Ekrana gelen tabloda 10.129.15.150:8080 -> 172.16.5.25:3389 eşleşmesini görmelisin).*

**3. Adım: Hedefe Bağlan (A Makinesinde)**
Artık kendi makinenden (A), B'nin dış IP'sine ve 8080 portuna RDP atıyorsun. B makinesi arkada bunu C'ye yönlendirecek.
```bash
xfreerdp /v:10.129.15.150:8080 /u:victor /p:pass@123
```
*(Görseldeki komutta senin lab IP'n farklı olabilir, kendi B makinenin dış IP'sini yazmalısın).*

---

**💡 Gerçek Hayat Notu:** 
Bu yöntemi gerçek sızma testlerinde bir Windows makinesi ele geçirdiğinde ve dışarıya dosya (Socat, Chisel vb.) atamadığında/yükleyemediğinde kullanırsın. Çünkü `netsh` Windows'un içinde hazır gelir, antivirüsler (AV) tarafından pek engellenmez ve sistemde hiçbir iz bırakmadan port yönlendirme yapmanı sağlar.