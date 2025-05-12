/* Senaryo:
Bir web sitesine veya uygulamaya kayıt (register) olurken, sistem genellikle kullanıcıdan sadece temel bilgileri (email/username ve password) alır.
Arka planda ise kullanıcının abonelik durumu (subscription) gibi ekstra bilgiler varsayılan bir değerle (örneğin "inactive") otomatik olarak ayarlanır.
*/

// Kullanıcıdan alınan örnek istek:
{
  "username": "test@test.com",
  "password": "test"
}

// Arka planda sistemin kaydettiği veri:
{
  "username": "test@test.com",
  "password": "test",
  "subscription": "inactive"  // Varsayılan olarak eklenir
}

/* 
  İstisna Durum:
  Eğer API, kullanıcının subscription alanını manuel olarak göndermesine izin veriyorsa, aşağıdaki gibi bir istek yapılabilir:
*/
{
  "username": "test@test.com",
  "password": "test",
  "subscription": "active"  // Kullanıcı tarafından manuel olarak ekleniyor
}

/*
Önemli Noktalar:

1. Default Değerler:
   Çoğu sistem, "subscription" gibi alanların kullanıcı tarafından belirlenmesine izin vermez. Örneğin, ücretsiz kayıt olan bir kullanıcı
   "subscription: active" göndererek premium özelliklere erişmeye çalışabilir. Bu bir güvenlik açığı oluşturabilir.

2. API Dokümantasyonu Kontrolü:
   Eğer "subscription" alanını gönderebiliyorsanız, bu durum API'nin dökümantasyonunda belirtilmiş olmalıdır.
   Belirtilmemişse, bu bir güvenlik açığına işaret edebilir.

3. Backend Mantığı:
   Genellikle "subscription" durumu, kullanıcı ödeme yaptıktan sonra backend tarafından "active" olarak güncellenir.
*/
fed5c695a46340ae48e3ea6601734951
