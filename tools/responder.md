# Responder Nedir ve Linux'ta Kullanimi

## Responder Nedir?

**Responder**, yerel ağ (LAN) üzerindeki kimlik doğrulama trafiğini hedef alarak kullanıcı adı ve parola hashlerini ele geçirmeye yarayan bir penetration testing aracıdır. Özellikle Windows ağlarındaki aşağıdaki protokolleri hedef alır:

- **LLMNR (Link-Local Multicast Name Resolution)**
- **NBT-NS (NetBIOS Name Service)**
- **mDNS (Multicast DNS)**

Bir kullanıcı yanlışlıkla bir sunucu adını çözümlemeye çalıştığında (örneğin \\SHARE gibi), Responder bu isteğe sahte bir sunucu gibi yanıt verip kullanıcının kimlik bilgilerini ele geçirmeye çalışır.

## Ne İşe Yarar?

- SMB, HTTP, LDAP gibi protokoller üzerinden gelen kimlik bilgilerini yakalar.
- Ele geçirilen şifre özetlerini (NTLMv1/v2 hash) sonradan **brute-force** veya **crack** için kullanabilirsiniz.
- Aktif saldırı ("rogue" servisleri sunma) ve pasif dinleme destekler.

## Kurulum

Responder, Kali Linux gibi birçok pentesting dağıtımında yüklü gelir. Yüklü değilse şu şekilde yüklenebilir:

```bash
sudo apt update
sudo apt install responder
```

veya GitHub üzerinden:

```bash
git clone https://github.com/lgandx/Responder.git
cd Responder
```

## Temel Kullanım

En basit haliyle çalıştırmak için:

```bash
sudo responder -I [INTERFACE]
```

Örnek:

```bash
sudo responder -I eth0
```

- `-I` : Hangi network arayüzünde (interface) çalışacağını belirtir (örneğin `eth0`, `wlan0`).

## Sık Kullanılan Parametreler

| Parametre | Açıklama |
|:---|:---|
| `-I` | Dinleme yapılacak network arayüzü |
| `-v` | Detaylı (verbose) çıktı |
| `-f` | Fake proxy sunucusu sunar |
| `-w` | WPAD saldırısı yapar |
| `-r` | NBT-NS ve LLMNR'ye yanıt verir |
| `-d` | Dinleme sırasında kimlik doğrulama hashlerini kaydeder |
| `-F` | SMB ve HTTP "auth" isteklerini zorunlu kılar |

Örnek gelişmiş kullanım:

```bash
sudo responder -I eth0 -v -f -w -r -d
```

## Gelişmiş Kullanım Parametreleri

| Parametre | Açıklama |
|:---|:---|
| `-b` | SMB Signing korumalarını bypass etmeye çalışır |
| `-P` | Özel bir WPAD (Web Proxy Auto-Discovery Protocol) sunucusu yapılandırır |
| `-A` | Responder'ın "Analyze mode" özelliği ile ağı tarayıp zayıflıkları tespit eder (aktif saldırı yapmadan) |
| `-e [file]` | Dışa aktarılan log dosyasını özelleştirir |
| `-t` | Hedef IP'yi belirtir (sadece belirli bir makineyi hedef almak için) |

### Örnekler

**SMB Signing Bypass Denemesi:**

```bash
sudo responder -I eth0 -b
```

**Özel WPAD Ayarı ile Çalıştırma:**

```bash
sudo responder -I eth0 -P CustomWPAD.dat
```

**Analyze Mode (Pasif Zayıflık Tespiti):**

```bash
sudo responder -I eth0 -A
```

## Kullanım Senaryosu

1. **Responder'ı Başlat:**

    ```bash
    sudo responder -I eth0
    ```

2. **Ağa bağlı kurban makine, yanlış bir hostname çözümlemeye çalışır.**

3. **Responder, sahte yanıt vererek kurbanı kendine yönlendirir.**

4. **Kurban makine, kimlik bilgilerini gönderir.**

5. **Responder bu bilgileri kaydeder.**

6. **Hash dosyası `Responder/logs/` dizininde bulunur.**

## Hashleri Crack Etme

Yakalanan hashleri **John the Ripper** veya **Hashcat** ile kırabilirsiniz.

Örnek (John kullanımı):

```bash
john --format=netntlmv2 hash_dosyasi.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

## Dikkat Edilmesi Gerekenler

- Responder kullanmak bazı ağlarda **alarm** tetikleyebilir (IDS/IPS sistemleri).
- İç ağda yetkilendirme gerekebilir.
- Yasal yetki olmadan kullanılması **suç** teşkil eder!

## Faydalı Linkler

- [Responder GitHub Sayfası](https://github.com/lgandx/Responder)
- [Responder Kullanım Kılavuzu (Wiki)](https://github.com/lgandx/Responder/wiki)

---

Bu dosya bir "eğitim" ve "bilgi" amacıyla hazırlanmıştır. Gerçek sistemlerde sadece **izinli testlerde** kullanılmalıdır.

---

**Hazırlayan:** _(Senin ismini/nikini buraya ekleyebilirsin)_

