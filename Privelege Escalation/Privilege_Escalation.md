
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

```bash
sudo -l
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
- find / -writable -type d 2>/dev/null 
- find . -name flag1.txt: geçerli dizinde “flag1.txt” adlı dosyayı bulun
- find /home -name flag1.txt: /home dizinindeki “flag1.txt” dosya adlarını bulun
- find / -type d -name config: “/” altında config adlı dizini bulun
- find / -type f -perm 0777: 777 izinlerine sahip dosyaları bul (tüm kullanıcılar tarafından okunabilir, yazılabilir ve çalıştırılabilir dosyalar)
- find / -perm a=x: çalıştırılabilir dosyaları bul
- find /home -user frank: “frank” kullanıcısına ait tüm dosyaları “/home” altında bul
- find / -mtime 10: Son 10 günde değiştirilen dosyaları bul
- find / -atime 10: Son 10 günde erişilen dosyaları bul
- find / -cmin -60: Son bir saat (60 dakika) içinde değiştirilen dosyaları bul
- find / -amin -60: Son bir saat (60 dakika) içinde erişilen dosyaları bul
- find / -size 50M: 50 MB boyutundaki dosyaları bul
Bu komut, belirtilen boyuttan daha büyük veya daha küçük bir dosyayı belirtmek için (+) ve (-) işaretleriyle birlikte de kullanılabilir.

``` bash
find . -name flag1.txt
```
Dosyayı geçerli kullanıcıdan daha yüksek bir ayrıcalık seviyesiyle çalıştırmamızı sağlayan SUID bitine sahip dosyaları bulun.
``` bash
find / -perm -u=s -type f 2>/dev/null
```
---








