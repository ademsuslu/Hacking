🟠 10. Directory Traversal (Path Traversal)
Açıklama:

Kullanıcının dizin dolaşarak sunucudaki dosyalara erişmesine neden olur.

Örnek:

```bash
http://example.com/download.php?file=../../../../etc/passwd

```
Önleme:

realpath(), basename(), allowlist ile dosya doğrulaması yap.

