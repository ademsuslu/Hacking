/* Senaryo:
Bir web sitesine veya uygulamaya kayıt (register) olurken, sistem genellikle kullanıcıdan sadece temel bilgileri (email/username ve password) alır.
Arka planda ise kullanıcının subscription (abonelik) durumu gibi ekstra bilgiler varsayılan bir değerle (örneğin inactive) otomatik ayarlanır.
*/
```json  
{
  "username": "test@test.com",
  "password": "test"
}
```
# Arka planda sistem şu şekilde kaydeder:
{
  "username": "test@test.com",
  "password": "test",
  "subscription": "inactive"  // Default olarak eklenir
}

/* 
  İstisna Durum:
  Eğer API, kullanıcının subscription alanını manuel olarak göndermesine izin veriyorsa, siz şöyle bir istek yapabilirsiniz:
*/
{
"username":"test@test.com",
"password":"test",
  // biz burauya subscription kendimiz ekleyebiliriz
  "subscription":"active"
}
/*
Önemli Noktalar:
Default Değerler:
Çoğu sistem, subscription gibi alanları güvenlik nedeniyle kullanıcının belirlemesine izin vermez. Örneğin, ücretsiz kayıt olan biri subscription: active göndererek premium özelliklere sızmaya çalışabilir.

API Dökümantasyon Kontrolü:
Eğer subscription alanını gönderebiliyorsanız, bu API'nin dökümantasyonunda belirtilmiş olmalıdır. Aksi takdirde bu bir güvenlik açığı olabilir.

Backend Logic:
Genellikle subscription durumu, kullanıcı ödeme yaptıktan sonra backend tarafından active olarak güncellenir.
*/
