Tarayıcı Güvenlik Özellikleri:
# Same-Origin Policy (SOP) nedir?
Same-Origin Policy (SOP), web güvenliği açısından önemli bir tarayıcı güvenlik mekanizmasıdır. Bu politika, bir kaynağın (örneğin bir web sayfasının) başka bir kaynağın verilerine yalnızca aynı kökene (origin) sahip olması durumunda erişmesine izin verir. Origin; protokol (örneğin HTTP veya HTTPS), domain (örneğin example.com) ve port numarasının birleşiminden oluşur.

SOP'un Temel Amacı
Same-Origin Policy, kötü niyetli web sitelerinin kullanıcıya ait hassas verilere (örneğin çerezlere, oturum bilgilerine veya tarayıcıda depolanan verilere) erişmesini önlemek için tasarlanmıştır. Örneğin, bir site kullanıcının banka hesabına ait oturum çerezlerini ele geçirmeye çalışıyorsa SOP devreye girer ve farklı bir kökene sahip olduğu için bu erişimi engeller.

SOP Nasıl Çalışır?
Bir tarayıcıda yüklü bir web sayfası, aşağıdaki koşullarda başka bir kaynağa erişebilir:

Protokol aynı olmalı (örneğin, her iki site de https kullanıyor olmalı).
Domain aynı olmalı (örneğin, www.example.com ile example.com farklıdır).
Port numarası aynı olmalı (örneğin, https://example.com:443 ile https://example.com:8080 farklıdır).
Örneğin:

https://example.com/page1 sayfası, https://example.com/page2'ye erişebilir çünkü kökenler aynıdır.
Ancak https://example.com sayfası, http://example.com ya da https://anotherdomain.com üzerindeki kaynaklara SOP nedeniyle doğrudan erişemez.

SOP'u Aşmanın Yolları
Bazı durumlarda SOP'nin katı kuralları esnetilmek istenir. Bunun için güvenli yöntemler kullanılır:

CORS (Cross-Origin Resource Sharing): Bir sunucu, başka bir kökenden gelen isteklere izin verebilir. Bu, yanıt başlıklarında gerekli izinleri tanımlayarak yapılır.
JSONP: SOP'un devrede olmadığı eski durumlar için kullanılan bir tekniktir, ancak artık pek güvenli değildir ve modern projelerde tercih edilmez.
Özetle:
Same-Origin Policy, web uygulamalarında güvenliğin temel taşlarından biridir ve tarayıcıların zararlı çapraz site işlemlerini engellemesine yardımcı olur. Ancak, belirli durumlarda CORS gibi yöntemlerle bu kısıtlamalar kontrollü bir şekilde aşılabilir.

# Content Security Policy (CSP) nedir?
Content Security Policy (CSP), web uygulamalarında güvenliği artırmak için kullanılan bir tarayıcı güvenlik mekanizmasıdır. CSP, geliştiricilere bir web sayfasının hangi kaynaklardan içerik yükleyebileceğini belirleme imkânı tanır. Bu, özellikle Cross-Site Scripting (XSS) ve diğer kod enjeksiyon saldırılarını önlemek için geliştirilmiş bir güvenlik politikasıdır.

CSP'nin Temel Amacı
CSP'nin temel amacı, kötü niyetli kodların web sayfasında çalıştırılmasını engelleyerek kullanıcı verilerini korumaktır. Bu, saldırganların sahte komut dosyalarını, stil dosyalarını ya da diğer kötü amaçlı içerikleri sayfaya dahil etmelerini zorlaştırır.

CSP Nasıl Çalışır?
CSP, HTTP yanıt başlıkları (Content-Security-Policy) veya <meta> etiketleri aracılığıyla tarayıcıya gönderilen bir dizi kuraldan oluşur. Bu kurallar, hangi kaynaklardan hangi tür içeriklerin yüklenebileceğini tanımlar. Örneğin:

JavaScript dosyalarının yalnızca belirli bir kaynaktan yüklenmesi.
Görsellerin yalnızca HTTPS üzerinden güvenli kaynaklardan gelmesi.
İçeriklerin inline (sayfa içinde gömülü) çalışmasının tamamen yasaklanması.
CSP Kuralları Örneği
Aşağıda bir CSP başlığının örneği verilmiştir:

plaintext
Copy code
Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.example.com; img-src https:;
Bu başlık şu kuralları uygular:

default-src 'self': Varsayılan olarak tüm kaynaklar yalnızca aynı kökenden (self) yüklenebilir.
script-src 'self' https://apis.example.com: JavaScript dosyaları yalnızca aynı kökenden (self) veya https://apis.example.com üzerinden yüklenebilir.
img-src https: Görseller sadece HTTPS kullanan kaynaklardan yüklenebilir.
CSP'nin Sağladığı Avantajlar
XSS Saldırılarını Engeller: Tarayıcı yalnızca izin verilen kaynaklardan içerik yükler, böylece saldırganların kötü amaçlı komut dosyaları eklemesi engellenir.
Kaynakların Kontrolü: Hangi kaynakların kullanılıp kullanılamayacağı geliştiriciler tarafından belirlenir.
Politika İzleme: CSP'nin bir "raporla" modu da vardır. Bu mod, saldırı girişimlerini algılar ve raporlar gönderir, böylece politika uygulanmadan önce test yapılabilir.
CSP Politikası Direktifleri
CSP'de kullanılan bazı yaygın direktifler şunlardır:

default-src: Varsayılan kaynak yükleme politikası.
script-src: JavaScript kaynakları için kısıtlamalar.
style-src: CSS dosyaları için kısıtlamalar.
img-src: Görseller için kısıtlamalar.
connect-src: Fetch, XHR veya WebSocket bağlantıları için kısıtlamalar.
font-src: Yazı tipleri için kısıtlamalar.
media-src: Video ve ses kaynakları için kısıtlamalar.
CSP'nin Zorlukları
Yanlış bir CSP yapılandırması, uygulamanın işlevselliğini bozabilir (örneğin, gerekli kaynakların engellenmesi).
Inline JavaScript ve stil kullanımı yasaklandığı için mevcut projelere entegre etmek zahmetli olabilir.
Üçüncü taraf hizmetleriyle entegrasyon (örneğin, reklam platformları) karmaşıklaşabilir.
CSP'nin Uygulama Örnekleri
Apache veya Nginx Konfigürasyonu: Bir CSP başlığı HTTP sunucusunda aşağıdaki gibi tanımlanabilir:

apache
Copy code
Header set Content-Security-Policy "default-src 'self'; script-src 'self' https://trusted-scripts.com;"
HTML Dosyasında Kullanım: HTML'de <meta> etiketiyle CSP tanımlanabilir:

html
``````
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self';">
Sonuç
Content Security Policy, web uygulamalarında güvenliği artırmak için oldukça etkili bir yöntemdir. Doğru yapılandırıldığında, XSS gibi yaygın saldırılara karşı güçlü bir koruma sağlar. Ancak, düzgün çalışması için detaylı planlama ve test süreci gerektirir.


 # CORS Nedir ne işe yarar 

CORS (Cross-Origin Resource Sharing), web uygulamalarında farklı kökenlerden (origin) gelen kaynaklara erişim için kullanılan bir tarayıcı güvenlik mekanizmasıdır. CORS, bir web sayfasının kendi kökeni dışında (örneğin başka bir domain, port veya protokol) bulunan kaynaklara erişmesine izin verirken, aynı zamanda bu erişimi kontrol altına almayı sağlar.

Bypass için:  cors-anywhere 

2.2 XSS Örneklerini İncele
 + Gerçek hayattan XSS açıkları ve CVE raporlarını incele.
 + OWASP XSS Cheat Sheet’e göz at.
 + Büyük güvenlik bloglarından (PortSwigger, HackerOne) XSS ile ilgili makaleleri oku.



CTF Platformları:
PicoCTF, OverTheWire gibi platformlarda XSS pratikleri yap.



4.2 Güvenlik Önlemleri ve Bypass Teknikleri
 + CSP Bypass:
    - CSP’nin nasıl çalıştığını ve nasıl aşılacağını öğren.  
 + Input Sanitization Bypass:
    - Giriş doğrulamasını aşmak için kullanılan teknikler.
 + WAF Bypass:
    - Web Application Firewall (WAF) sistemlerini kandırma yöntemleri.
