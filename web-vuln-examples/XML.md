9. XML External Entity (XXE) Attack
Açıklama:

XML işleyen uygulamalarda, saldırganın harici XML varlıkları tanımlayarak sunucu dosyalarını okumasına izin verir.

Örnek:

```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```
Önleme:

XML işlemede disable external entities kullan.