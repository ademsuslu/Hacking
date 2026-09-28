# PHP Type Juggling - Magic Hash Bypass

## Zafiyet Nedir?

PHP'de `==` operatörü "loose comparison" yapar. İki string de "numeric string" formatındaysa (yani `0e123456` gibi bilimsel gösterime uyan bir formatta), PHP bunları **karakter karakter değil, sayı olarak** karşılaştırır.

Bu yüzden `md5(X) == md5(Y)` gibi bir karşılaştırmada, X ve Y birbirinden tamamen farklı stringler olsa bile, eğer ikisinin de md5 hash'i `0e` + sadece rakamlardan oluşuyorsa, PHP ikisini de matematiksel olarak `0`'a indirger ve `true` döner.

## Örnek

```
echo -n "QNKCDZO" | md5sum
=> 0e830400451993494058024219903391

echo -n "ABJIHVY" | md5sum
=> 0e462097431906509019562988736854
```

İki farklı input, iki farklı görünen hash. Ama format aynı: `0e` + sadece rakam.

PHP bu formatı görünce bilimsel gösterim (scientific notation) sanıyor:

```
0e830400451993494058024219903391 => 0 * 10^830400451993494058024219903391
0e462097431906509019562988736854 => 0 * 10^462097431906509019562988736854
```

<strong style='color:red'>Üssü ne olursa olsun, 0 ile çarpılan her şey 0'a eşit. Yani:</strong>

```
0 == 0 => true
```

Gerçek bir kriptografik hash çakışması yok, PHP'nin tip dönüşümü (type juggling) yüzünden oluşan bir mantık hatası var.

## Zafiyetli Kod Örneği

```php
<?php
$secret_hash = md5($secret); // örn: md5("QNKCDZO")

if (md5($_GET['input']) == $secret_hash) {
    echo "FLAG";
}
```
**burada doğru cevap:** `ABJIHVY`

`$secret`'ı bilmesen bile, `$secret_hash`'in `0e` + rakam formatında olduğunu tahmin edip (veya biliyorsan), hazır bir "magic hash" listesinden aynı formatta md5 üreten başka bir string bulup gönderirsen bypass olur.

## Bypass Koşulu

- Karşılaştırma `==` ile yapılmalı (`===` ise çalışmaz, çünkü tip kontrolü de yapılır)
- Her iki hash de `0e` + sadece rakam formatında olmalı
- Kullandığın input, secret'ın kendisi olmak zorunda değil — sadece aynı "magic hash" formatını üreten farklı bir string olması yeterli

## Not

Bu teknik sadece md5'e özel değil, sha1() gibi diğer hash fonksiyonlarında da aynı mantıkla "magic hash" çakışmaları bulunabilir.