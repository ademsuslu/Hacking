# enum4linux-ng

## Temel Kullanım

```bash
enum4linux-ng 10.129.14.128 -A
```

## Parametreler

- `-A`: Tüm standart enumeration modüllerini açar (kullanıcılar, gruplar, paylaşımlar, parola politikası vb.).
- `-C`: Null session ile yapılabilecek ek kontrolleri çalıştırır (oturum izinleri gibi).

## Örnek

```bash
enum4linux-ng 10.10.11.45 -A -C
```

## Dikkat Edilecekler

- Anonim erişim (null session) var mı?
- Açık paylaşımlar ve içerikleri
- Kullanıcı listesi
- Parola politikası (lockout eşiği)

