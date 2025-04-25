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
