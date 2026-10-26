# Proxychains ile Terminal Trafiğini Burp Suite'e Yönlendirme (Orta Seviye Rehber)

Bu rehber, Linux işletim sistemlerinde kendi proxy ayarı bulunmayan komut satırı araçlarının (CLI) trafiğini **Proxychains** kullanarak **Burp Suite** üzerine nasıl yönlendireceğinizi ve bu istekleri nasıl manipüle edeceğinizi anlatmaktadır.

---

## 📌 Temel Mantık Nedir?

*   **Tarayıcılar (Firefox/Chrome):** Kendi içlerinde proxy ayarlarına sahip olduklarından trafiği doğrudan Burp Suite'e gönderebilirler.
*   **Terminal Araçları (curl, nmap, sqlmap, gobuster):** Sistem proxy ayarlarını genellikle göz ardı ederler ve doğrudan hedefe bağlanırlar.
*   **Proxychains:** Terminal araçlarının önüne eklenerek, o aracın işletim sistemi seviyesindeki ağ çağrılarını yakalar ve zorla Burp Suite'e yönlendirir.

---

## 🛠️ 1. Yapılandırma Adımları

Modern Linux dağıtımlarında (Kali Linux, Parrot OS vb.) Proxychains-ng (v4) sürümü kurulu gelir.

### Adım 1: Yapılandırma Dosyasını Açın
Terminalde root yetkileriyle şu komutu çalıştırın:
```bash
sudo nano /etc/proxychains4.conf
```

### Adım 2: Sessiz Modu Aktif Edin (Tavsiye Edilir)
Proxychains varsayılan olarak her bağlantı girişimini terminale loglar. Bu durum `gobuster` veya `sqlmap` gibi araçlarda ekranın kirlenmesine neden olur. Bunu engellemek için şu satırı bulun ve başındaki `#` işaretini kaldırın:
```text
quiet_mode
```

### Adım 3: Burp Suite Proxy Tanımını Ekleyin
Dosyanın en altına (`[ProxyList]` başlığının altına) inin. Mevcut tanımları yorum satırı yapın (`#`) ve Burp Suite'in varsayılan adresini ekleyin:
```text
[ProxyList]
# socks4  127.0.0.1 1080 (Varsayılanı yorum satırı yaptık)
http 127.0.0.1 8080
```
*Dosyayı kaydetmek için: `Ctrl + O` -> `Enter` -> `Ctrl + X`*

---

## 🚀 2. Orta Seviye Kullanım Senaryoları

### Senaryo A: curl ile İstek Başlıklarını (Headers) İnceleme
Bir web sayfasına `curl` ile istek atarken arka planda giden `User-Agent` veya `Cookie` bilgilerini Burp üzerinde görmek ve değiştirmek için:

```bash
proxychains4 curl -X GET http://example.com
```

### Senaryo B: sqlmap İsteklerini Manipüle Etme (WAF Atlatma)
Otomatik SQL enjeksiyon taraması yaparken, `sqlmap`'in gönderdiği payload'ların hedef sunucu tarafından nasıl yorumlandığını (veya engellendiğini) Burp Suite'in **HTTP History** sekmesinden saniye saniye izleyebilirsiniz. 
*Ayrıca Burp'ün `Match and Replace` özelliğini kullanarak sqlmap isteklerine dinamik olarak yeni başlıklar ekleyebilirsiniz.*

```bash
proxychains4 sqlmap -u "http://target.local" --batch
```

### Senaryo C: Dizin Tarama Araçlarında Hız Sınırı (Rate Limit) Analizi
`gobuster` veya `dirb` gibi araçları Proxychains ile çalıştırırken dikkatli olunmalıdır. Çok hızlı istek atmak proxy'yi kilitleyebilir. Orta seviye bir analiz için thread (iş parçacığı) sayısı düşük tutulmalıdır:

```bash
proxychains4 gobuster dir -u http://target.local -w /usr/share/wordlists/dirb/common.txt -t 5
```

---

## ⚠️ Kritik Bilgiler ve Sınırlamalar

1.  **Statik Bağlı (Statically Linked) Binary Dosyaları:** Proxychains, dinamik kütüphane çağrılarını (`LD_PRELOAD`) manipüle ederek çalışır. Eğer çalıştırdığınız araç statik olarak derlenmişse (örneğin bazı Go dili ile yazılmış araçlar), Proxychains trafiği **yakalayamaz**. Bu durumda aracın kendi `--proxy` parametresi kullanılmalıdır.
2.  **Nmap ile Kullanım (Kısıtlama):** Nmap üzerinde SYN Scan (`-sS`) gibi ham soket (raw socket) kullanan taramalar Proxychains ile **çalışmaz**. Nmap trafiğini yönlendirmek için TCP Connect Scan (`-sT`) modunu ve DNS çözümlemesini devre dışı bırakan `-Pn` parametrelerini kullanmalısınız:
    ```bash
    proxychains4 nmap -sT -Pn -p 80,443 target.local
    ```

