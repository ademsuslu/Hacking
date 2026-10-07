# Linux'ta `dig` Komutu

Linux'ta **`dig` (Domain Information Groper)**, DNS (Domain Name System) sorguları yapmak için kullanılan bir komut satırı aracıdır. Genellikle ağ yöneticileri ve sistem yöneticileri tarafından DNS kayıtlarını kontrol etmek, IP adreslerini bulmak veya bir alan adının çözüleme sürecini incelemek için kullanılır.  

## **`dig` Komutunun Kullanımı**
**Temel sözdizimi:**
```bash
dig [alan_adı]
```
**Örnek:**
```bash
dig google.com
```
Bu komut, **google.com** alan adının A (IPv4 adresi) kaydını getirir.

# 🛡️ Bug Bounty İçin DNS Kayıtları Rehberi & Gelişmiş Subdomain Takeover Mantığı

Bug bounty süreçlerinde (özellikle keşif/recon aşamasında) karşına çıkacak kritik DNS kayıtları, bunların işlevleri ve **Subdomain Takeover** zafiyetiyle olan doğrudan bağları aşağıda listelenmiştir.

---

## 1. Temel DNS Kayıt Türleri

### 📌 CNAME (Canonical Name)
* **Nedir?:** Bir subdomain'i doğrudan bir IP'ye değil, başka bir alan adına (domain) yönlendirir. Takma ad (alias) oluşturur.
* **Hacker Gözüyle:** Subdomain Takeover zafiyetlerinin **%90'ının kaynağıdır.** Şirketler genellikle AWS, GitHub Pages, Zendesk, Shopify gibi üçüncü parti (third-party) servisleri kullanmak için CNAME kaydı açarlar.

### 📌 A (Address) / AAAA (Quad-A)
* **Nedir?:** Alan adını doğrudan bir IPv4 (`A`) veya IPv6 (`AAAA`) adresine bağlar.
* **Hacker Gözüyle:** Eğer bir subdomain bir IP'ye bakıyorsa ve o IP boşa çıktıysa (örneğin şirket sunucuyu kapatmış ama DNS kaydını silmemişse), o IP'yi bulut sağlayıcıdan yakalayarak sunucuyu ele geçirebilirsin.

### 📌 NS (Name Server)
* **Nedir?:** O subdomain veya domain'in DNS kayıtlarını hangi sunucunun yönettini söyler.
* **Hacker Gözüyle:** **"Subdomain Delegation Takeover"** adı verilen en yüksek ödüllü zafiyet türüne yol açar. Alt alan adının tüm DNS yönetim haklarını ele geçirmeyi sağlar.

### 📌 MX (Mail Exchange)
* **Nedir?:** E-posta sunucularını belirtir.
* **Hacker Gözüyle:** Boşta kalmış kurumsal e-posta servislerine yönlendirilmiş MX kayıtları üzerinden **Mail Takeover** yapılarak şirkete gelen e-postalar çalınabilir.

### 📌 TXT (Text)
* **Nedir?:** Kimlik doğrulama metinleri içerir (SPF, DKIM, DMARC, Google Site Verification).
* **Hacker Gözüyle:** `SPF` ve `DMARC` kayıtlarındaki eksiklikler incelenerek **Email Spoofing** (şirket adına sahte mail atma) zafiyeti aranır.

---

## 💀 Subdomain Takeover Çeşitleri ve Çalışma Mantığı

Subdomain Takeover, en basit tanımıyla bir **"Yetim DNS Kaydı (Dangling DNS)"** problemidir. Bir servis kapatılsa bile DNS panelinde kaydının unutulmasıyla tetiklenir.

### Yöntem 1: CNAME Tabanlı Bulut Servisi Takeover (En Yaygın)
1. **Senaryo:** `firma.com`, dökümantasyon sayfası için GitHub Pages kullanmaya karar verir ve `://firma.com` için bir **CNAME** kaydı oluşturup bunu `firma.github.io` adresine yönlendirir.
2. **Hata:** İki yıl sonra şirket projeyi iptal eder ve GitHub üzerindeki o sayfayı **siler**. Ancak DNS panelindeki CNAME kaydını kaldırmayı unutur.
3. **Saldırı:** Saldırgan kendi kişisel GitHub hesabında yeni bir depo açar ve "Custom Domain" kısmına `://firma.com` yazar. GitHub, CNAME kaydını doğrulayarak sayfayı saldırganın hesabına bağlar.

### Yöntem 2: A / AAAA Tabanlı IP Recycling Takeover
1. **Senaryo:** Şirket `://firma.com` adresini geçici bir bulut sunucusunun (AWS EC2, DigitalOcean Droplet vb.) IP adresine (`A` kaydı ile örn: `34.23.45.67`) bağlar.
2. **Hata:** Proje bittiğinde şirket AWS sunucusunu **siler/kapatır** ancak DNS panelindeki `A` kaydını temizlemez. Statik IP kullanılmadıysa, sunucu silindiğinde o IP havuzu serbest kalır ve başka müşterilere verilebilir hale gelir.
3. **Saldırı:** Saldırgan bulut sağlayıcı üzerinde sürekli yeni sunucular ayağa kaldırıp kapatarak (veya IP kiralama betikleri yazarak) `34.23.45.67` IP'sinin kendi hesabına atanmasını sağlar. IP eşleştiği an subdomain otomatik olarak saldırganın sunucusuna çıkar.

### Yöntem 3: NS Tabanlı Nameserver Delegation Takeover (Kritik/Yüksek Ödül)
1. **Senaryo:** Büyük şirketler, alt departmanların (örn: pazarlama) kendi DNS kayıtlarını yönetebilmesi için `://firma.com` adresine **NS kayıtları** tanımlayarak yetkiyi AWS Route 53 veya Azure DNS gibi bulut servislerine devreder.
2. **Hata:** Pazarlama ekibi işi bitince AWS Route 53 üzerindeki DNS Bölgesini (Hosted Zone) siler. Ancak ana şirketin ağ yöneticisi ana panelden bu NS kayıtlarını kaldırmaz.
3. **Saldırı:** AWS Route 53 gibi servisler açılan her bölgeye rastgele isim sunucuları atar. Saldırgan kendi AWS hesabında sürekli `://firma.com` adıyla yeni bölgeler açar. Ne zaman ki bulut sağlayıcının ona atadığı NS sunucuları ile şirketin boştaki NS kayıtları çakışırsa, **tüm subdomain yönetimi ve alt subdomain açma yetkisi** saldırgana geçer.

### Yöntem 4: MX Tabanlı Mail Takeover
1. **Senaryo:** Şirket kurumsal e-posta altyapısı veya bülten/pazarlama e-posta sunucuları için üçüncü parti bir servis kullanıyordur ve `MX` kaydını oraya yönlendirmiştir.
2. **Hata:** Şirket servis aboneliğini iptal eder fakat DNS panelindeki `MX` kaydını silmeyi unutur.
3. **Saldırı:** Saldırgan söz konusu e-posta sağlayıcısında bir hesap açar ve şirketin alan adını kendi profiline tanımlar. `MX` kaydı zaten oraya baktığı için, o domaine gönderilen tüm kurumsal veya şifre sıfırlama gibi kritik e-postalar saldırganın gelen kutusuna düşer.

---

## 💡 Hızlı Karşılaştırma Tablosu

| Kayıt Türü | Zafiyet Adı | Tespit Yöntemi | Zorluk Derecesi | Ödül Potansiyeli |
| :--- | :--- | :--- | :--- | :--- |
| **CNAME** | Cloud Service Takeover | `dig CNAME` -> 404/Bulut hata mesajı | Kolay | Medium / High |
| **A / AAAA** | Bulut IP Geri Dönüşüm Takeover | `dig A` -> Sahipsiz bulut IP'si | Zor (IP yakalamak şans/otomasyon ister) | High |
| **NS** | Nameserver Hijacking | `dig NS` -> Cevap vermeyen / Boşta kalan AWS/Azure NS'leri | Orta / Zor | Critical / High |
| **MX** | Mail Hijacking | `dig MX` -> Yetim e-posta sunucu kayıtları | Orta | High |

---

## 🛠️ `dig` İle Pratik Avcılık Komutları

* **Sadece CNAME kayıtlarını filtrelemek için:**
  ```bash
  dig CNAME ://subdomain.com +short
  ```
* **NS kayıtlarında sahipsiz yetki aramak için:**
  ```bash
  dig NS ://hedefdomain.com
  ```
* **E-posta zafiyetleri için MX kayıtlarına bakmak için:**
  ```bash
  dig MX hedefdomain.com
  ```
* **Hızlıca tüm kayıtları (Any) dökmek için:**
  ```bash
  dig ANY hedefdomain.com
  ```
