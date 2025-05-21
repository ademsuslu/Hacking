# Blind SQLi
Saldırımızın sonuçlarını doğrudan ekranda görebildiğimiz Bant İçi SQL enjeksiyonundan farklı olarak, 
kör SQLi, enjekte edilen sorgularımızın gerçekten başarılı olup olmadığını doğrulamak için çok az veya hiç geri bildirim almadığımız zamandır,
bunun nedeni hata mesajlarının devre dışı bırakılmış olmasıdır, ancak enjeksiyon yine de çalışır.
Tüm bir veritabanını başarıyla numaralandırmak için ihtiyacımız olan tek şeyin bu küçük geri bildirim olması sizi şaşırtabilir.


# Authentication Bypass:
En basit Kör SQL Enjeksiyon tekniklerinden biri, oturum açma formları gibi kimlik doğrulama yöntemlerini atlatmaktır.
Bu durumda, veritabanından veri almakla ilgilenmiyoruz; sadece oturum açmayı geçmek istiyoruz. 
Kullanıcıların bir veritabanına bağlı olan oturum açma formları genellikle web uygulamasının kullanıcı adı ve parolanın içeriğiyle değil,
daha çok bu ikisinin kullanıcılar tablosunda eşleşen bir çift oluşturup oluşturmadığıyla ilgilendiği şekilde geliştirilir.
Temel olarak, web uygulaması veritabanına "bob kullanıcı adı ve bob123 parolasına sahip bir kullanıcınız var mı?" diye sorar.
Veritabanı evet veya hayır (doğru/yanlış) şeklinde yanıt verir ve bu yanıta bağlı olarak web uygulamasının devam etmenize izin verip vermeyeceğini belirler. 
Yukarıdaki bilgileri göz önünde bulundurarak, geçerli bir kullanıcı adı/şifre çifti saymak gereksizdir. Sadece evet/doğru ile yanıt veren bir veritabanı sorgusu oluşturmamız gerekiyor.


#Practic
Pratik:

SQL Enjeksiyonu örneklerinin İkinci Seviyesi tam olarak bu örneği gösterir.
" SQL Sorgusu" etiketli kutuda veritabanına yapılan sorgunun şu olduğunu görebiliriz:


```bash
select * from users where username='%username%' and password='%password%' LIMIT 1;
```
***#NB  %username%  ve  %password%  değerleri oturum açma formu alanlarından alınmıştır. SQL Sorgu kutusundaki başlangıç ​​değerleri, bu alanlar şu anda boş olduğundan boş olacaktır.***
