Mysql default port 3306'dır
Mysql giriş ssl sertifikaları devre dısı: 
```bash
mysql -u root -p -h 10.10.192.39 --ssl=no   
```
```bash
mysql -u kullanici_adi -p -h localhost -P 3306
```

##  Tüm veritabanlarını listele:
```bash
SHOW DATABASES;
```


##   Bir veritabanı seç:
```bash
USE veritabani_adi;
```


##  Seçili veritabanındaki tabloları listele:
```bash
SHOW TABLES;
```

##  Seçili veritabanındaki tabloların içini gör:
```bash
SELECT * FROM tablo_adi ;
```
