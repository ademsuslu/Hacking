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

## **Önemli `dig` Parametreleri**
| Komut | Açıklama |
|--------|------------|
| `dig google.com` | Google'ın IP adresini çözümler (varsayılan olarak A kaydı). |
| `dig google.com MX` | Google'ın **Mail Exchange (MX)** kayıtlarını listeler. |
| `dig google.com NS` | Alan adının **ad sunucularını (Name Servers - NS)** gösterir. |
| `dig google.com TXT` | Alan adının **TXT kayıtlarını** gösterir (SPF, DKIM gibi doğrulamalar için kullanılır). |
| `dig google.com ANY` | Tüm DNS kayıtlarını getirir (bazı sunucular kısıtlamış olabilir). |
| `dig @1.1.1.1 google.com` | **Cloudflare DNS** sunucusunu kullanarak sorgu yapar. |
| `dig +short google.com` | Sadece IP adresini gösterir. |
| `dig +trace google.com` | Alan adının çözüleme sürecini detaylı gösterir. |

## **Örnek Çıktı**
```bash
$ dig google.com
```
```txt
; <<>> DiG 9.16.1-Ubuntu <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;google.com.            IN      A

;; ANSWER SECTION:
google.com.     299     IN      A       142.250.74.206

;; Query time: 30 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Fri Mar 28 12:00:00 UTC 2025
;; MSG SIZE  rcvd: 55
```
Bu çıktıda **google.com** alan adının **142.250.74.206** IP adresine çözümlendiğini görebiliriz.

Eğer daha fazla detaylı inceleme yapmak istiyorsan, belirli bir DNS sunucusunu kullanarak sorgular yapabilir veya `+trace` seçeneğini deneyebilirsin.

# Linux'ta Avanced `dig` Komutu

**zone transfer ile transfer edileni görürüz**

```bash
dig -t TXT key.z.hackycorp.com

; <<>> DiG 9.20.15-2-Debian <<>> -t TXT key.z.hackycorp.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2794
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;key.z.hackycorp.com.           IN      TXT

;; ANSWER SECTION:
key.z.hackycorp.com.    43200   IN      TXT     "9f883f22-6ea5-4631-bbe8-95841ad63f56"

;; Query time: 144 msec
;; SERVER: 192.168.1.1#53(192.168.1.1) (UDP)
;; WHEN: Tue Dec 23 14:00:49 +03 2025
;; MSG SIZE  rcvd: 97
```

**Şirketlerin gizleyebileceği verileri görmek için**
```bash
dig AXFR z.hackerone.com # => fail
dig -t SOA z.hackerone.com # => ;z.hackycorp.com.               IN      SOA
dig -t AXFR z.hackerone.com @z.hackerone.com # => z.hackerone.com 
```
**araştır**
```bash
dig -t NS z.hackycorp.com
dig AXFR int @z.hackycorp.com

```
