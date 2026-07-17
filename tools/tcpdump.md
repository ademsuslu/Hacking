# tcpdump kullanımı

### ctfler için ilk shell aldıkdan sonra kullabilir

```bash
ip a


# output
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen
1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host noprefixroute
valid_lft forever preferred_lft forever

2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen
1000
link/ether 00:50:56:94:46:f8 brd ff:ff:ff:ff:ff:ff
altname enp3s0
altname ens160
inet 10.129.24.166/16 brd 10.129.255.255 scope global dynamic eth0
valid_lft 3161sec preferred_lft 3161sec
inet6 dead:beef::250:56ff:fe94:46f8/64 scope global dynamic mngtmpaddr
valid_lft 86399sec preferred_lft 14399sec
inet6 fe80::250:56ff:fe94:46f8/64 scope link
valid_lft forever preferred_lft forever

br-1b6b4b93c636: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdi
sc noqueue state UP
group default
link/ether ca:86:2c:ad:e3:06 brd ff:ff:ff:ff:ff:ff
inet 172.25.0.1/16 brd 172.25.255.255 scope global br-1b6b4b93c636
valid_lft forever preferred_lft forever
inet6 fe80::c886:2cff:fead:e306/64 scope link

```


```bash
tcpdump -i br-1b6b4b93c636 -A -s 0 tcp                                    
```
                                                                              
•  `-i` br-...  → dinlenecek arayüz (konteynerlerin bağlı olduğu bridge).     
•  `-A`  → paket içeriğini ASCII olarak yazdırır (düz metin cred'leri görmek için).                                                                      
•  `-s 0`  → paketi tam boyutta yakalar (kırpma yok).                         
•  tcp  → sadece TCP filtresi. 