# Dependency Confusion (Bağımlılık karmaşası)

1. **Hedef Tespiti**: Saldırgan, ilk aşamada hedef şirketin kullandığı özel (private) kütüphanelerin isimlerini belirler. Bu isimler genellikle şirketin halka açık web sitelerindeki JavaScript dosyalarında (özellikle package.json içinde) veya internete sızmış yapılandırma dosyalarında bulunur.

2. **Kötü Amaçlı Paket Hazırlığı**: Saldırgan, şirketin kullandığı özel kütüphane ile tam olarak aynı isme sahip bir kütüphane oluşturur. Ancak bu kütüphaneyi npm, pip veya RubyGems gibi genel (public) paket depolarına yükler.

3. **Sürüm Numarası Manipülasyonu**: Yazılım yükleme araçları (pip gibi), aynı isme sahip iki paketle karşılaştığında genellikle en yüksek sürüm numarasına sahip olanı seçer. Saldırgan, genel depoya yüklediği sahte pakete çok yüksek bir sürüm numarası (örneğin 99.9.9) vererek, şirketin kendi özel kütüphanesinden daha "güncel" görünmesini sağlar.

4. **Otomatik İndirme ve Kod Çalıştırma**: Şirketin sunucuları veya geliştiricilerin bilgisayarları paketleri güncellerken veya yeni projeler oluştururken, sistem otomatik olarak genel depodaki bu "yüksek sürüm numaralı" sahte paketi çeker ve yükler.

5. **Veri Sızdırma**: Paket yüklendiği anda içerisindeki kötü amaçlı kod (installation script) çalışmaya başlar. Şirketin güvenlik duvarı HTTP trafiğini engellese bile, saldırgan bu bilgileri (sistem adı, kullanıcı bilgisi vb.) DNS protokolü üzerinden sorgular göndererek kendi sunucusuna sızdırır. Böylece sistemde Uzaktan Kod Çalıştırma (RCE) elde edilmiş olur.
