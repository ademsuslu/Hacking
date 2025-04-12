## 🔍 Port Dinleme Analizi (CTF Notları)

### Komut:
```bash
ss -tpln | grep "8111"
```
Açıklama:
Bu komut, sistemde çalışan servisler arasında 8111 numaralı TCP portunu dinleyen uygulamayı bulur.

ss Parametreleri:
-t → Yalnızca TCP bağlantılarını listeler

-p → Portu kullanan işlemi gösterir

-l → Dinleyen (listening) portları gösterir

-n → IP ve portları çözümlemeden gösterir (daha hızlı)

Örnek Çıktı:
```bash
LISTEN 0 100 [::ffff:127.0.0.1]:8111
```
Açıklama:
LISTEN: Port aktif olarak dinleniyor.

0 100: Kuyruk durumu (bağlantı detayları).
```bash
[::ffff:127.0.0.1]:8111:
```
127.0.0.1: Localhost (sadece makine içinden erişilebilir).

8111: Dinlenen port numarası.

🎯 Not:
Bu port sadece localhost üzerinden erişilebilen bir servise aittir. Dışarıdan erişim mümkün değildir.

💡 Çözüm:
Portu dış dünyaya erişilebilir kılmadan test etmek için SSH port forward kullanılabilir.

SSH Tünelleme:
```bash
ssh -L 8111:127.0.0.1:8111 user@target-ip
```
Bu şekilde kendi bilgisayarında localhost:8111 üzerinden uzak makinedeki servise erişebilirsin.

🧪 Ekstra Kontroller:
Portta ne çalıştığını görmek için aşağıdaki komutlar kullanılabilir:

```bash
lsof -i :8111
```
``` bash
netstat -tulpen | grep 8111
```
``` bash
ps aux | grep 8111
```




