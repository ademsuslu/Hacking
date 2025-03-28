 5. Server-Side Request Forgery (SSRF)
Açıklama:

Sunucunun, saldırgan tarafından belirlenen URL'lere istek yapmasını sağlar.

İç ağ servislerine veya metadata API'lere erişim sağlanabilir.

Örnek:
``` php
<?php
if (isset($_GET['url'])) {
    $url = $_GET['url'];  // Kullanıcıdan URL alınıyor (Filtreleme yok!)
    $response = file_get_contents($url);
    echo $response;
}
?>

```
🛑 SSRF Exploit (Saldırganın Kullanacağı URL'ler)
1️⃣ İç Ağ Tarama (Internal Network Scan)


```bash

Edit
http://hedefsite.com/vulnerable.php?url=http://127.0.0.1/admin

```
Ne Olur?

Hedef sunucu, saldırganın belirttiği URL'ye istekte bulunur.

Eğer iç ağda çalışan bir yönetim paneli (örn. http://127.0.0.1/admin) varsa, saldırgan içeriği okuyabilir.

2️⃣ AWS Metadata Servisinden Credential Çalma (Cloud Exploit)


```ruby

http://hedefsite.com/vulnerable.php?url=http://169.254.169.254/latest/meta-data/

```
Ne Olur?

Eğer hedef sunucu bir AWS EC2 instance’ı üzerinde çalışıyorsa, saldırgan AWS erişim anahtarlarını alabilir.

Örneğin, şu URL ile hassas bilgiler elde edilebilir:

```ruby
http://169.254.169.254/latest/meta-data/iam/security-credentials/

```
3️⃣ Docker & Kubernetes İç Ağına Erişim

```bash
http://hedefsite.com/vulnerable.php?url=http://172.17.0.1:2375/info

```
Ne Olur?

Eğer sunucu bir Docker konteyneri içinde çalışıyorsa, saldırgan Docker API'ye erişerek yeni container’lar oluşturabilir.

🛡️ SSRF Önleme Yöntemleri
✅ 1. URL Allowlist Kullan
Sadece güvenli URL'lere izin ver:

``` php

$allowed_domains = ['example.com', 'trustedsource.com'];
$parsed_url = parse_url($_GET['url']);
if (!in_array($parsed_url['host'], $allowed_domains)) {
    die("Yetkisiz istek!");
}

```
✅ 2. IP Filtering Kullan
Özel IP adreslerine istek yapılmasını engelle:

```php
if (preg_match('/^(127\.|10\.|172\.16\.|192\.168\.)/', $parsed_url['host'])) {
    die("Yetkisiz erişim!");
}
```
✅ 3. Web Güvenlik Duvarı (WAF) Kullan
Özellikle AWS gibi platformlarda AWS WAF veya Cloudflare kullanarak SSRF saldırılarını engelleyebilirsin.