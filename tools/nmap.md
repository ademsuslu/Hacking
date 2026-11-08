
# Firewall and IDS/IPS Evasion

## Firewalls
**Bir güvenlik duvarı, harici ağlardan gelen yetkisiz bağlantı girişimlerine karşı bir güvenlik önlemidir.**

## IPS/IDS

+ **saldırı ÖNLEME sistemi `(IPS)`**
+ **saldırı TESPIT sistemi `(IDS)`**


### SYN-scan (Synchronize - Tanışma/Bağlantı İsteği) `-sS`
#### Seninle bir bağlantı kurmak, iletişim başlatmak istiyorum

```bash
nmap 10.129.2.28 -p 21,22,25 -sS -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:56 CEST
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:22 S ttl=53 id=22412 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:25 S ttl=50 id=62291 iplen=44  seq=4092255222 win=1024 <mss 1460>
SENT (0.0278s) TCP 10.10.14.2:57347 > 10.129.2.28:21 S ttl=58 id=38696 iplen=44  seq=4092255222 win=1024 <mss 1460>
RCVD (0.0329s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=40884 iplen=72 ]
RCVD (0.0341s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
RCVD (1.0386s) TCP 10.129.2.28:22 > 10.10.14.2:57347 SA ttl=64 id=0 iplen=44  seq=1153454414 win=64240 <mss 1460>
SENT (1.1366s) TCP 10.10.14.2:57348 > 10.129.2.28:25 S ttl=44 id=6796 iplen=44  seq=4092320759 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up (0.0053s latency).

PORT   STATE    SERVICE
21/tcp filtered ftp
22/tcp open     ssh
25/tcp filtered smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

```

### ACK-Scan (Synchronize - Tanışma/Bağlantı İsteği) `-sA`
#### Gönderdiğin paketi (veya teklifi) sapasağlam aldım, onaylıyorum.

```bash
sudo nmap 10.129.2.28 -p 21,22,25 -sA -Pn -n --disable-arp-ping --packet-trace

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-21 14:57 CEST
SENT (0.0422s) TCP 10.10.14.2:49343 > 10.129.2.28:21 A ttl=49 id=12381 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:22 A ttl=41 id=5146 iplen=40  seq=0 win=1024
SENT (0.0423s) TCP 10.10.14.2:49343 > 10.129.2.28:25 A ttl=49 id=5800 iplen=40  seq=0 win=1024
RCVD (0.1252s) ICMP [10.129.2.28 > 10.10.14.2 Port 21 unreachable (type=3/code=3) ] IP [ttl=64 id=55628 iplen=68 ]
RCVD (0.1268s) TCP 10.129.2.28:22 > 10.10.14.2:49343 R ttl=64 id=0 iplen=40  seq=1660784500 win=0
SENT (1.3837s) TCP 10.10.14.2:49344 > 10.129.2.28:25 A ttl=59 id=21915 iplen=40  seq=0 win=1024
Nmap scan report for 10.129.2.28
Host is up (0.083s latency).

PORT   STATE      SERVICE
21/tcp filtered   ftp
22/tcp unfiltered ssh
25/tcp filtered   smtp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

```

##  Decoys `-D RND:5` 

+ `-D RND:5` istekleri 5 farklı ip adresinden gönder

```bash 
nmap 10.129.2.28 -p 80 -D RND:5
```


## Scan by Using Different Source IP `-S 10.10.10.10`
+ **`-S`**  parametresi, nmap ile gönderdiğiniz paketlerin üzerindeki "gönderen IP adresi" kısmını tamamen değiştirerek sahte bir IP adresi yazmanızı sağlar (IP Spoofing / IP Sahtekarlığı) 



```bash 
nmap 10.129.2.28 -p 80 -S 10.10.10.10
```


# DNS Proxying

## Kurnazlık (DNS Portunu Taklit Etme)

**örn:** `--source-port 53` 53 numaralı porttan (DNS servisinden)  geliyor

```bash
nmap 10.129.2.28 -p50000 --source-port 53

50000/tcp open  ibm-db2
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
```



Yukarıda 5000 porttunu acık oldugu için İçeri Sızma (Ncat ile Bağlantı)

```bash
ncat -nv --source-port 53 10.129.2.28 50000
```





---
# Host Scanning

## Listten alıp ping atma

```bash
nmap -sn -oA tnet -iL hosts.lst

```

+ **`-iL` input List yani hosts.lst** dosyasındaki herşeyi alır ping atar ve output olarak **nmap** **gnmap** **xml** olarak tnet dosyasına kaydeder

---

## multiple ips alıp ping atma

```bash
sudo nmap -sn -oA nmap_result 10.129.2.18 10.129.2.19 10.129.2.20 | grep for | cut -d" " -f5

```

+ **`-iL` input List yani hosts.lst** dosyasındaki herşeyi alır ping atar ve output olarak **nmap** **gnmap** **xml** olarak tnet dosyasına kaydeder

### farklı bir şekilde aynı işlem

```bash
sudo nmap -sn -oA nmap_result 10.129.2.18-20 | grep for | cut -d" " -f5
```

---


## Paketleri terminale yazma

```bash
sudo nmap 10.129.2.18 -sn -oA host -PE --packet-trace 

```

+ **`-PE`** standart ping taraması
+ **`--packet-trace`** Gönderilen ve alınan bütün paketleri terminale yazar 

---

## Paketleri terminale yazma

```bash
nmap 10.129.2.18 -sn -oA host -PE --reason 
```

+ **`-PE`** standart ping taraması
+ **`--reason`** Bana sadece portun açık veya kapalı olduğunu söyleme, bu sonuca tam olarak hangi pakete bakarak vardığını da açıkla


**örn:**
```bash
nmap 10.129.2.18 -sn -oA host -PE --reason 

PORT   STATE SERVICE REASON
22/tcp open  ssh     syn-ack
80/tcp open  http    syn-ack
```
---


## Address Resolution Protocol - Adres Çözümleme Protokolü

Bilgisayarlar aynı yerel ağ (LAN) içinde birbirleriyle iletişim kurarken sadece IP adreslerini kullanamazlar. Verinin doğru cihaza gitmesi için o cihazın fiziksel ağ kartı adresini, yani MAC adresini bilmek zorundadırlar.


```bash
sudo nmap 10.129.2.18 -sn -oA host -PE --packet-trace --disable-arp-ping 
```
+ **`--disable-arp-ping`** Hedefle aynı ağda olsak bile ARP sorgusuyla kolay yoldan cihazın açık olup olmadığını kontrol etme
**Arp mantığı**: IP adresini bir kişinin "Adı Soyadı" gibi düşünün. MAC adresini ise o kişinin "T.C. Kimlik Numarası" veya "Ev Adresi" gibi düşünebilirsiniz. Ağdaki router veya bilgisayarınız bağırır: "10.129.2.18 IP'sine sahip olan cihaz, senin MAC adresin ne?" Karşıdaki cihaz da kendi MAC adresini söyler. Bu işleme **ARP** denir.


# Host ve Port Scanning



| State | Description |
| --- | --- |
| open | Taranan portla bağlantının kurulduğunu gösterir. Bu bağlantılar TCP bağlantıları, UDP datagramları veya SCTP eşleşmeleri olabilir. |
| closed | Port kapalı olarak gösterildiğinde, TCP protokolü geri aldığımız paketin bir RST bayrağı içerdiğini belirtir. Bu tarama yöntemi, hedefimizin canlı olup olmadığını belirlemek için de kullanılabilir. |
| filtered | Nmap, taranan portun açık mı yoksa kapalı mı olduğunu doğru bir şekilde tanımlayamaz; çünkü port için hedeften ya hiçbir yanıt dönmez ya da hedeften bir hata kodu alınır. |
| unfiltered | Bir portun bu durumu yalnızca TCP-ACK taraması sırasında ortaya çıkar ve portun erişilebilir olduğu anlamına gelir, ancak açık mı yoksa kapalı mı olduğu belirlenemez. |
| open\|filtered | Belirli bir port için yanıt alamazsak, Nmap bu durumu atayacaktır. Bu durum, bir güvenlik duvarının veya paket filtresinin portu koruyor olabileceğini gösterir. |
| closed\|filtered | Bu durum yalnızca IP ID idle taramalarında ortaya çıkar ve taranan portun bir güvenlik duvarı tarafından kapalı mı yoksa filtrelenmiş mi olduğunu belirlemenin imkansız olduğunu gösterir. |



## Top 10 portu tarama

```bash
sudo nmap 10.129.2.18 --top-ports=10 
```

---
## Top 10 portu tarama

```bash
sudo nmap 10.129.2.28 -p 21 --packet-trace -Pn -n --disable-arp-ping

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:39 CEST
SENT (0.0429s) TCP 10.10.14.2:63090 > 10.129.2.28:21 S ttl=56 id=57322 iplen=44  seq=1699105818 win=1024 <mss 1460>
RCVD (0.0573s) TCP 10.129.2.28:21 > 10.10.14.2:63090 RA ttl=64 id=0 iplen=40  seq=0 win=0
Nmap scan report for 10.129.2.28
Host is up (0.014s latency).

PORT   STATE  SERVICE
21/tcp closed ftp
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
```

### Request (İstek) Tablosu

| Message | Description |
| --- | --- |
| SENT (0.0429s) | Nmap'in hedefe bir paket gönderdiği gönderme (SENT) işlemini belirtir. |
| TCP | Hedef portla etkileşime geçmek için kullanılan protokolü gösterir. |
| 10.10.14.2:63090 > | Nmap tarafından paketleri göndermek için kullanılacak olan IPv4 adresimizi ve kaynak portu temsil eder. |
| 10.129.2.28:21 | Hedef IPv4 adresini ve hedef portu gösterir. |
| S | Gönderilen TCP paketinin SYN bayrağıdır (Bağlantı isteği). |
| ttl=56 id=57322 iplen=44 seq=1699105818 win=1024 mss 1460 | Ek TCP Başlık (Header) parametreleridir. |

### Response (Yanıt) Tablosu

| Message | Description |
| --- | --- |
| RCVD (0.0573s) | Hediften alınan (received) paketi belirtir. |
| TCP | Kullanılmakta olan protokolü gösterir. |
| 10.129.2.28:21 > | Yanıt vermek için kullanılacak olan hedefin IPv4 adresini ve kaynak portunu temsil eder. |
| 10.10.14.2:63090 | Yanıt verilecek olan IPv4 adresimizi ve portu gösterir. |
| RA | Gönderilen TCP paketinin RST (Sıfırla) ve ACK (Onayla) bayraklarıdır (Portun kapalı olduğunu gösterir). |
| ttl=64 id=0 iplen=40 seq=0 win=0 | Ek TCP Başlık (Header) parametreleridir. |



+ **`-Pn`** Ping Atmayı Devre Dışı Bırak / No Ping
+ **`-n`** DNS Çözümlemesini Devre Dışı Bırak / No DNS Resolution

---


## Connect Scan on TCP Port 443

```bash
sudo nmap 10.129.2.28 -p 443 --packet-trace --disable-arp-ping -Pn -n --reason -sT 

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:26 CET
CONN (0.0385s) TCP localhost > 10.129.2.28:443 => Operation now in progress
CONN (0.0396s) TCP localhost > 10.129.2.28:443 => Connected
Nmap scan report for 10.129.2.28
Host is up, received user-set (0.013s latency).

PORT    STATE SERVICE REASON
443/tcp open  https   syn-ack

```

+ **`-sT`** scan tcp

---

## Filtered Ports

```bash
sudo nmap 10.129.2.28 -p 139 --packet-trace -n --disable-arp-ping -Pn --max-retries=10

Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 15:45 CEST
SENT (0.0381s) TCP 10.10.14.2:60277 > 10.129.2.28:139 S ttl=47 id=14523 iplen=44  seq=4175236769 win=1024 <mss 1460>
SENT (1.0411s) TCP 10.10.14.2:60278 > 10.129.2.28:139 S ttl=45 id=7372 iplen=44  seq=4175171232 win=1024 <mss 1460>
Nmap scan report for 10.129.2.28
Host is up.

PORT    STATE    SERVICE
139/tcp filtered netbios-ssn
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)

```

+ **`--max-retries=10`** Bu, Nmap'ın önceki paketin yanlışlıkla yanlış yapılıp yapılmadığını belirlemek için talebi hedef porta 10 kere yeniden göndereceği anlamına gelir. 

---


## Discovering Open UDP Ports `-sU`

```bash
nmap 10.129.2.28 -F -sU


Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-15 16:01 CEST
Nmap scan report for 10.129.2.28
Host is up (0.059s latency).
Not shown: 95 closed ports
PORT     STATE         SERVICE
68/udp   open|filtered dhcpc
137/udp  open          netbios-ns
138/udp  open|filtered netbios-dgm
631/udp  open|filtered ipp
5353/udp open          zeroconf
MAC Address: DE:AD:00:00:BE:EF (Intel Corporate)
```

+ **`-F`** scan top 100 ports

---

## Version Scan `-sV`

```bash
sudo nmap 10.129.2.28 -Pn -n --disable-arp-ping --packet-trace -p 445 --reason  -sV
```

# nmap sonuçlarını kaydetme

1. `-oN` normal output **result.nmap**
2. `-oG` normal output **result.gnmap**
3. `-oX` normal output **result.xml**

## xml cıktısını htmle Dönüştürme


```bash
xsltproc nmap_result.xml -o nmap_result.html
```


# Service Enumeration

## Service Version Detection `-sV`

```bash
nmap 10.129.2.28 -p- -sV
```

### `--stats-every=5s` her 5 saniyede ilerlemeyi gösterir

```bash
nmap 10.129.2.28 -p- -sV --stats-every=5s
```
### `-v`  ayrıntılı bir şekilde ekrar olan biteni yazar

```bash
nmap 10.129.2.28 -p- -sV --stats-every=5s
```

--- 

# Nmap Scripting Engine `-sC`


| Category | Description |
| :--- | :--- |
| auth | Kimlik doğrulama bilgilerinin belirlenmesi. |
| broadcast | Ağda yayın (broadcast) yaparak canlı cihaz keşfi için kullanılan betikler; keşfedilen cihazlar otomatik olarak kalan taramalara eklenebilir. |
| brute | Kayıtlı kimlik bilgileriyle kaba kuvvet (brute-force) saldırısı düzenleyerek ilgili servise giriş yapmayı deneyen betikleri çalıştırır. |
| default | `-sC` parametresi kullanıldığında çalıştırılan varsayılan betikler. |
| discovery | Erişilebilir durumdaki ağ servislerinin değerlendirilmesi ve incelenmesi. |
| dos | Servis dışı bırakma (Denial of Service - DoS) açıklarını kontrol etmek için kullanılan betiklerdir; servislere zarar verebileceği için daha az tercih edilirler. |
| exploit | Taranan port üzerindeki bilinen güvenlik açıklarını doğrudan istismar etmeye (exploit etmeye) çalışan betik kategorisi. |
| fuzzer | Farklı veri alanları göndererek beklenmedik paket işleme durumlarını ve zafiyetleri tespit etmeye çalışan betiklerdir; tamamlanması uzun zaman alabilir. |
| intrusive | Hedef sistemi olumsuz yönde etkileyebilecek (agresif/müdahaleci) betikler. |
| malware | Hedef sisteme herhangi bir zararlı yazılım (malware) bulaşıp bulaşmadığını kontrol eder. |
| safe | Hedefe müdahaleci veya yıkıcı bir erişimde bulunmayan, savunma/güvenlik odaklı betikler. |
| version | Servis ve versiyon tespiti için kullanılan genişletilmiş betikler. |
| vuln | Belirli ve spesifik güvenlik açıklarının (zafiyetlerin) tanımlanması ve tespit edilmesi. |


### Specific Scripts Category
```bash
nmap <target> --script <category>
```

### Defined Scripts

```bash
nmap <target> --script <script-name>,<script-name>
```


### Nmap - Specifying Scripts

```bash
nmap 10.129.2.28 -p 25 --script banner,smtp-commands
```

# Nmap - Aggressive Scan `-A`

**`-A`** şu aşağıdakileri aynı anda çalıştırır

+ **Açık Portların Versiyon Tespiti `-sV`**
+ **Varsayılan Betik Taraması `-sC`**
+ **İşletim Sistemi Tespiti `-O`**
+ **Yol İzleme (Traceroute)**


```bash
nmap 10.129.2.28 -p 80 -A
```

# Vulnerability Assessment

## Nmap - Vuln Category `--script vuln `

```bash
nmap 10.129.2.28 -p 80 -sV --script vuln 

Nmap scan report for 10.129.2.28
Host is up (0.036s latency).

PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-enum:
|   /wp-login.php: Possible admin folder
|   /readme.html: Wordpress version: 2
|   /: WordPress version: 5.3.4
|   /wp-includes/images/rss.png: Wordpress version 2.2 found.
|   /wp-includes/js/jquery/suggest.js: Wordpress version 2.5 found.
|   /wp-includes/images/blank.gif: Wordpress version 2.6 found.
|   /wp-includes/js/comment-reply.js: Wordpress version 2.7 found.
|   /wp-login.php: Wordpress login page.
|   /wp-admin/upgrade.php: Wordpress login page.
|_  /readme.html: Interesting, a readme.
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| http-wordpress-users:
| Username found: admin
..
<SNIP>
```

# Performance

## Timeouts 

**default**
```bash
nmap 10.129.2.0/24 -F
```
**Optimized**
```bash
nmap 10.129.2.0/24 -F --initial-rtt-timeout 50ms --max-rtt-timeout 100ms
```
- `--initial-rtt-timeout 50ms` Nmap, hedefteki bir porta ilk paketi fırlattığında, karşı taraftan yanıt gelmesi için **en başta ne kadar süre bekleyeceğini belirler.**
- `--max-rtt-timeout 50ms` Nmap, hedefteki bir porta ilk paketi fırlattığında, karşı taraftan yanıt gelmesi için **eMaksimum Bekleme Süresi**

## Max Retries `--max-retries`
**Her portun kapısını sadece 1 kere çal**

**Default**
```bash
 nmap 10.129.2.0/24 
```

**Reduced Retries**
```bash
sudo nmap 10.129.2.0/24 -F --max-retries 0 
```
## Rates `--min-rate 5000`
**Ağda ne olursa olsun, bağlantı kalitesi ne kadar kötü olursa olsun, yavaşlama! Saniyede en az 5000 paket göndereceksin. Bu hızın altına asla düşme!**

**Min Rate**

```bash
nmap 10.129.2.0/24 -F -oN tnet.minrate300 --min-rate 5000
```


# Timing `-T`


+ `-T 0` / `-T paranoyak`
+ `-T 1` / `-T sinsi`
+ `-T 2` / `-T Kibar`
+ `-T 3` / `-T normal`
+ `-T 4` / `-T Agrasif`
+ `-T 5` / `-T imkansız`

**example**

```bash
nmap 10.129.2.0 -T 3
```


# Nmap Kullanımı ve Port Taramaları

## CP-SYN taraması (-sS), SYN bayrağına sahip tek bir paket gönderir bu nedenle üç adımlı el sıkışma (three-way handshake) sürecini tamamlamaz ve sonuç olarak taranan portla tam bir TCP bağlantısı kurulmamış olur.

+ Hedefimiz bize `SYN-ACK` bayraklı bir paket gönderirse, Nmap portun açık olduğunu tespit eder.
+ Eğer hedef, `RST` bayraklı bir paketle yanıt verirse, bu durum portun kapalı olduğunun bir göstergesidir.
+ Nmap herhangi bir yanıt paketi alamazsa, portu `filtered` olarak işaretler.

```bash
nmap -sS localhost
```



## 0. **Hızlı biraz detaylı tarama**
```bash
nmap 10.10.1.0 p -sVC -T4 -oN nmap.txt
```
Bu komut, hedefte açık olan portların hızlıca tarar.
---


## 1. **Temel Tarama**
```bash
nmap 10.10.137.90
```
Bu komut, hedefte açık olan temel TCP portlarını kontrol eder.

---

## 2. **Servis ve Versiyon Bilgisi**
```bash
nmap -sV 10.10.137.90
```
Bu komut, açık portlarda hangi servislerin çalıştığını ve servislerin versiyon bilgilerini gösterir.

---

## 3. **Detaylı Tarama (Aggressive Scan)**
```bash
nmap -A 10.10.137.90
```
Bu tarama, servis versiyon bilgilerini, işletim sistemi tespiti ve traceroute gibi ek bilgileri verir.

---

## 4. **Belirli Portları Hedefleme**
Sadece belirli portları taramak istersen:
```bash
nmap -p 21,22,80,443 10.10.137.90
```
Bu komut, belirttiğin portları (ör. FTP, SSH, HTTP, HTTPS) tarar.

---

## 5. **UDP Port Tarama**
UDP portlarını kontrol etmek için:
```bash
nmap -sU 10.10.137.90
```
Bu komut UDP portları üzerinde hangi servislerin çalıştığını kontrol eder.

---

## 6. **Tüm Portları Tarama**
Tüm portları taramak için:
```bash
nmap -p- 10.10.137.90
```
Bu komut, 1-65535 arasındaki tüm portları tarar.

---

## 7. **Script Tarama (NSE Kullanarak)**
Nmap'in script motoruyla daha spesifik testler yapabilirsin. Örneğin, HTTP servisinde zafiyet taraması yapmak için:
```bash
nmap --script http-vuln* 10.10.137.90
```
script, kullanma :
```bash
nmap --script=ftp-anon -p 21 10.10.72.54 -Pn -vv
```



---
## 8. **Operatig system scan**
hedefin kullandığı işletim sistemini bulmak için:
```bash
nmap -O [ip]
```


---
## 9. **Service version scan**
hedefte çalışan servislerin sürümünü algılamak için bir anahtar sağlar:
```bash
nmap -Sv [ip]
```

---
## 10. **Port aralıklarını tarama**
hedefte çalışan port aralığını taramayı sağlar:
```bash
nmap -p 100-300 [ip]
```
---

## 11. **script kullanımı**
"Vuln" kategorisindeki tüm scriptleri nasıl aktifleştirirsiniz?:
```bash
nmap --script=vuln [ip]
```
---
## 12. **script bulma**
Scriptleri nereden buluruz?:
```bash
ls -l /usr/share/nmap/scripts/*ftp*
```
## 13. sadece ping atma

```
 nmap 10.129.2.0/24 -sn -oA tnet | grep for | cut -d" " -f5
```
+ `-sn` sadece ping atar port taraması yapmaz
+ `10.129.2.0/24` burada `10.129.2.0`-`10.129.2.255` arası ping atar
+ `-oA tnet` output olarak `-oA` olduğu için All yani 3 farklı cıktı verir **namp** **gnmap** **xml** `tnet` cıktı dosyasının ismi
