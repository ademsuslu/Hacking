# dnsenum

## dnsenum ile dns 
```bash
 dnsenum --dnsserver 10.129.14.128 --enum -p 0 -s 0 -o subdomains.txt -f /opt/useful/seclists/Discovery/DNS/subdomains-top1million-110000.txt inlanefreight.htb
```
# Domain Name System (`DNS`)

## DNS Türleri

| Sunucu Türü | Açıklama |
|---|---|
| **DNS Root Server** | Üst düzey alan adlarından (TLD) sorumludur. Bir isim sunucusu son çare olarak sorgulanmadıkça devreye girmez; alan adı ile IP adresi arasında internette merkezi bir arayüz görevi görür. ICANN, kök isim sunucularının çalışmasını koordine eder. Dünya genelinde 13 adet kök sunucu vardır. |
| **Authoritative Nameserver** | Belirli bir bölge (zone) için yetkilidir. Yalnızca kendi sorumluluk alanındaki sorguları yanıtlar ve bu alandaki bilgileri bağlayıcıdır (kesin). Bir yetkili isim sunucusu sorguyu yanıtlayamazsa, sorgu kök isim sunucusuna devredilir. Ülke, şirket vb. bilgilere göre yetkili isim sunucuları, özyinelemeli DNS sunucularına yanıt vererek belirli web sunucusunu bulmaya yardımcı olur. |
| **Non-authoritative Nameserver** | Belirli bir DNS bölgesinden sorumlu değildir. Bunun yerine belirli DNS bölgeleri hakkındaki bilgileri toplar. Özyinelemeli veya yinelemeli (iterative) DNS sorgulamasıyla çalışır. |
| **Caching DNS Server** | Diğer isim sunucularından alınan bilgileri belirli bir süre önbellekte tutar. Bu depolamanın süresini yetkili isim sunucusu belirler. |
| **Forwarding Server** | Yalnızca bir işlev görür: DNS sorgularını başka bir DNS sunucusuna iletir. |
| **Resolver** | Yetkili DNS sunucusu değildir. Ancak isim çözümlemesini bilgisayarda veya yönlendiricide yerel olarak gerçekleştirir. |

**Pratikte fark:** Yetkili sunucu bilginin "kaynağıdır", önbellek sunucusu ise bu bilgiyi geçici olarak tutar. Bug bounty'de subdomain keşfi yaparken, bir sorgunun yetkili bir sunucudan mı yoksa önbellekten mi yanıtlandığını ayırt etmek, DNS kayıtlarının güncelliğini değerlendirmek açısından önemlidir.


## DNS kayıtları
| Kayıt (Record) | Açıklama |
|---|---|
| `A` | İstenen alan adının IPv4 adresini döndürür. |
| `AAAA` | İstenen alan adının IPv6 adresini döndürür. |
| `MX` | Sorumlu posta sunucularını döndürür. |
| `NS` | Alan adının DNS sunucularını (nameserver) döndürür. |
| `TXT` | Çeşitli bilgiler içerebilir. Google Search Console veya SSL sertifikası doğrulamasında kullanılabilir. Ayrıca SPF ve DMARC kayıtları da bu tip ile tanımlanır ve posta trafiğini doğrulayarak spam'e karşı korur. |
| `CNAME` | Bir alan adı için başka bir alan adına takma ad (alias) görevi görür. Örneğin `www.hackthebox.eu` için hem `hackthebox.eu` adına bir `A` kaydı hem de `www.hackthebox.eu` adına bir `CNAME` kaydı oluşturulabilir. |
| `PTR` | Ters sorgulama (reverse lookup) yapar. IP adreslerini geçerli alan adlarına dönüştürür. |
| `SOA` | İlgili DNS bölgesi ve yönetici iletişim e-posta adresi hakkında bilgi verir. |

**Bug bounty açısından notlar:**

- **`NS` ve `SOA`** kayıtları, alan adının hangi yetkili sunucularda yönetildiğini ve yönetici e-posta adresini gösterir. Yanlış yapılandırılmış bir `NS` kaydı ya da bölge transferine açık bir sunucu, kapsamlı bilgi sızıntısına yol açabilir.
- **`TXT`** kayıtlarında bazen API anahtarı, doğrulama tokenları veya iç servis bilgileri bulunabilir. Bu kayıtları incelemek keşif aşamasında faydalıdır.
- **`CNAME`** kayıtları, kullanılmayan bir hizmete işaret ediyorsa subdomain takeover riski doğurabilir. Bu, bug bounty'de sık raporlanan bir bulgu türüdür.
- **`MX`** kayıtları, mail altyapısının hangi sağlayıcıda olduğunu gösterir ve e-posta güvenliği (SPF/DMARC) değerlendirmesinde kullanılır.

### example soa

```bash
dig soa www.inlanefreight.com

; <<>> DiG 9.16.27-Debian <<>> soa www.inlanefreight.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15876
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 1, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 512
;; QUESTION SECTION:
;www.inlanefreight.com.         IN      SOA

;; AUTHORITY SECTION:
inlanefreight.com.      900     IN      SOA     ns-161.awsdns-20.com. awsdns-hostmaster.amazon.com. 1 7200 900 1209600 86400

;; Query time: 16 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Thu Jan 05 12:56:10 GMT 2023
;; MSG SIZE  rcvd: 128
```
**awsdns-hostmaster.amazon.com => awsdns-hostmaster@amazon.com**


## Default Configuration

### Local Dns Confgiration

```bash
cat /etc/bind/named.conf.local

//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";
zone "domain.com" {
    type master;
    file "/etc/bind/db.domain.com";
    allow-update { key rndc-key; };
};

```
### Zone Files

```bash
 cat /etc/bind/db.domain.com

;
; BIND reverse data file for local loopback interface
;
$ORIGIN domain.com
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

      IN     MX     10     mx.domain.com.
      IN     MX     20     mx2.domain.com.

             IN     A       10.129.14.5

server1      IN     A       10.129.14.5
server2      IN     A       10.129.14.7
ns1          IN     A       10.129.14.2
ns2          IN     A       10.129.14.3

ftp          IN     CNAME   server1
mx           IN     CNAME   server1
mx2          IN     CNAME   server2
www          IN     CNAME   server2
```

### Reverse Name Resolution Zone Files

```bash
cat /etc/bind/db.10.129.14

;
; BIND reverse data file for local loopback interface
;
$ORIGIN 14.129.10.in-addr.arpa
$TTL 86400
@     IN     SOA    dns1.domain.com.     hostmaster.domain.com. (
                    2001062501 ; serial
                    21600      ; refresh after 6 hours
                    3600       ; retry after 1 hour
                    604800     ; expire after 1 week
                    86400 )    ; minimum TTL of 1 day

      IN     NS     ns1.domain.com.
      IN     NS     ns2.domain.com.

5    IN     PTR    server1.domain.com.
7    IN     MX     mx.domain.com.
...SNIP...

```

## Dangerous Settings

| Seçenek | Açıklama |
|---|---|
| `allow-query` | DNS sunucusuna sorgu gönderebilecek hostları belirler. |
| `allow-recursion` | DNS sunucusuna özyinelemeli (recursive) sorgu gönderebilecek hostları belirler. |
| `allow-transfer` | DNS sunucusundan bölge transferi (zone transfer) alabilecek hostları belirler. |
| `zone-statistics` | Bölgelerin istatistiksel verilerini toplar. |

**Güvenlik açısından dikkat edilecekler:**

- **`allow-transfer`** en kritik ayardır. Herkese açık ya da `any` olarak bırakılmışsa, bir saldırgan `dig axfr @<sunucu> <alan_adı>` ile tüm alan adı kayıtlarını (iç host adları, IP'ler, test sunucuları) tek seferde indirebilir. Bug bounty'de bölge transferi açıklığı sık görülen ve değerli bir bulgudur.
- **`allow-recursion`** herkese açıksa sunucu açık resolver olarak kötüye kullanılabilir. Bu, DNS amplifikasyon (DDoS) saldırılarına zemin hazırlar.
- **`allow-query`** kısıtlı değilse, sunucunun tüm kayıtlarını herkes sorgulayabilir. Yetkili sunucularda genellikle herkese açık olması normaldir, ancak iç DNS sunucularında kısıtlanması gerekir.
- **`zone-statistics`** tek başına kritik değildir, ancak bölge istatistikleri içerdiği için keşif aşamasında ek bilgi sağlayabilir.
