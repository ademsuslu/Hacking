🟤 8. Insecure Direct Object References (IDOR)
Açıklama:

Kullanıcı kimlik doğrulaması yapılmadan, doğrudan başka bir kaynağa erişim sağlanmasıdır.

Örnek:

```bash
http://example.com/user?id=5
```

Burada kullanıcı başka birinin bilgilerini görebilir id 1 yerine farklı ieyler girildiğinde.

Önleme:

Kimlik doğrulama ve yetkilendirme mekanizmaları kullan.