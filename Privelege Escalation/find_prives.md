Komutu bul
Hedef sistemde önemli bilgiler ve potansiyel ayrıcalık yükseltme vektörleri aramak verimli olabilir. Dahili "find" komutu kullanışlıdır ve cephaneliğinizde bulundurmaya değer.


Aşağıda “find” komutu için bazı yararlı örnekler verilmiştir.
Dosyaları bul:
Dosyayı geçerli kullanıcıdan daha yüksek bir ayrıcalık seviyesiyle çalıştırmamızı sağlayan SUID bitine sahip dosyaları bulun.
``` bash
find / -perm -u=s -type f 2>/dev/null
```


hataları "/dev/null"a yönlendirmek ve daha temiz bir çıktı elde etmek için "find" komutunu "-type f 2>/dev/null" ile kullanmak akıllıca olacaktır 



- ```bash 
  find / -user root -perm /4000  2>/dev/null
  ```
  # (***oldukça öenmli)
- ``` bash find / -type f -perm -04000 -ls 2>/dev/null ```
- groups sogrusu 
  - ``` bash find / -type f -group bugtracker 2> /dev/null ```
- ``` bash find / -writable -type d 2>/dev/null ```
  # : geçerli dizinde “flag1.txt” adlı dosyayı bulun
- ``` bash find . -name flag1.txt```
  #: /home dizinindeki “flag1.txt” dosya adlarını bulun
- ``` bash find /home -name flag1.txt```
   #: “/” altında config adlı dizini bulun
- ``` bash find / -type d -name config```
   # : 777 izinlerine sahip dosyaları bul (tüm kullanıcılar tarafından okunabilir, yazılabilir ve çalıştırılabilir dosyalar)
- ``` bash find / -type f -perm 0777```
  # : çalıştırılabilir dosyaları bul
- ``` bash find / -perm a=x ```
  #: “frank” kullanıcısına ait tüm dosyaları “/home” altında bul 
- ``` bash find /home -user frank ```
  # : Son 10 günde değiştirilen dosyaları bul
- ``` bash find / -mtime 10 ```
  #: Son 10 günde erişilen dosyaları bul
- ``` bash find / -atime 10 ```
  #: Son bir saat (60 dakika) içinde değiştirilen dosyaları bul
- ``` bash find / -cmin -60 ```
  #: Son bir saat (60 dakika) içinde erişilen dosyaları bul
- ``` bash find / -amin -60 ```
  #: 50 MB boyutundaki dosyaları bul
- ``` bash find / -size 50M  ```
Bu komut, belirtilen boyuttan daha büyük veya daha küçük bir dosyayı belirtmek için (+) ve (-) işaretleriyle birlikte de kullanılabilir.

``` bash
find . -name flag1.txt
```
