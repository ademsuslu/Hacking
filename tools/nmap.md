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
