
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
