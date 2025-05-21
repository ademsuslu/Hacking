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
