# PHP intval() ve is_numeric() Zafiyetleri

## 1. intval() - Integer Overflow

`intval()` bir stringi sayıya çevirirken PHP'nin taşıyabileceği maksimum integer sınırını (`PHP_INT_MAX` = `9223372036854775807`, 64-bit sistemde) aşan değerleri **overflow** ederek hep aynı max değere sabitler.

```php
var_dump(intval("99999999999999999999999999999999")); 
// int(9223372036854775807)

var_dump(intval("88888888888888888888888888888888")); 
// int(9223372036854775807)

var_dump(intval("99999999999999999999999999999999") === intval("88888888888888888888888888888888"));
// bool(true) - iki farklı dev sayı overflow sonrası eşitleniyor
```

### Nerede işe yarar
```php
if (intval($_GET['id']) === intval($secret_id)) {
    // $secret_id bilinmese bile, PHP_INT_MAX'i aşan HERHANGİ bir sayı
    // gönderilerek eşleşme sağlanabilir (secret'ın da çok büyük olduğu varsayımıyla)
}
```

Saldırgan gerçek gizli değeri bilmese bile, aynı overflow noktasına düşen bir sayı göndererek eşleşme sağlayabilir. Tek koşul: hedef değerin de `PHP_INT_MAX`'i aşan bir sayı olduğunu tahmin edebilmek.

---

## 2. intval() - Baştaki Sayıyı Okuyup Gerisini Kesme

```php
intval("1000abc") // => 1000
intval("3x3e8")    // => 3
```

`intval()` string'in başındaki geçerli sayısal kısmı okur, geçersiz karakter görünce durur. Format/validasyon kontrollerini bypass etmek için kullanılabilir (örnek: "1000abc" bir regex'i geçebilir ama intval sonrası hep 1000'e döner).

---

## 3. is_numeric() - Bilimsel Gösterimi Kabul Etmesi

`is_numeric()` bilimsel gösterim formatını (`1e9`, `2e10` gibi) **geçerli sayı** sayar.

```php
is_numeric("1e9")  // true
intval("1e9")      // 1000000000  (1 milyar!)
strlen("1e9")      // 3  (string olarak sadece 3 karakter)
```

### Neden tehlikeli
Bir kod hem `is_numeric()` ile "sayı mı" kontrolü yapıp, hem de `strlen()` ile "kaç haneli" diye uzunluk sınırlaması yapıyorsa, bu ikisi birbirini yanlış tamamlar:

```php
if (!is_numeric($_POST["age"])) {
    $errors[] = 'Geçersiz yaş';
}
if (strlen($_POST["age"]) > 3) {
    $errors[] = 'Yaş çok uzun';
}
$age = intval($_POST["age"]);
```

`"1e9"` gönderilirse:
- `is_numeric("1e9")` → `true`, kontrolü geçer
- `strlen("1e9")` → `3`, uzunluk kontrolünü de geçer (string olarak 3 karakter)
- `intval("1e9")` → `1000000000`, **gerçek değer 10 haneli**

Yani "maksimum 3 haneli sayı" kısıtlaması tamamen bypass edilmiş oldu, gerçek değer 10 hane.

## 4. Bu ikisinin birleşimi: Fixed-width parsing bypass

Eğer bir sistem, verileri `substr()` ile sabit offset/uzunluklarda parse ediyorsa (örn. bir text formatında: username 15 karakter, password 32 karakter, age 3 karakter...) ve `age` gibi bir alanın uzunluğunu `str_pad()` ile "sabitlediğini" varsayıyorsa:

```php
$line .= str_pad($age, 3, "#"); // varsayım: age hep 3 karakter olacak
```

**Önemli:** `str_pad()` sadece verilen değer hedef uzunluktan **kısaysa** doldurma yapar. Değer zaten hedef uzunluktan **uzunsa hiçbir şey yapmaz, kesmez.**

```php
str_pad("1000000000", 3, "#"); // => "1000000000" (kesilmiyor, 10 karakter kalıyor)
```

Yani `age` alanına `is_numeric`/`strlen` kontrollerini geçen ama `intval` sonrası uzun bir sayıya dönüşen bir değer (`1e9` gibi) verilirse, o alandan sonraki tüm alanların (`firstname`, `lastname`, admin flag gibi) **başlangıç index'i kayar.**

### Index hesaplama mantığı
Her alanın başlangıç index'i = kendinden önceki tüm alanların toplam uzunluğu.

Normal offsetler bozulduğunda, sabit index'ten okuyan parse fonksiyonu (`substr($data, 112, 1)` gibi) artık **beklenen alanı değil, kayma sonucu oraya denk gelen başka bir alanın içeriğini** okur. Saldırgan, kayma miktarını hesaplayıp, kendi kontrolündeki bir alana (örn. `lastname`) hedef pozisyona denk gelecek karakteri (`Y` gibi) yerleştirebilir.

**Ders:** `is_numeric()` bir değerin "kaç haneli" olacağını garanti etmez, `str_pad()` kesme yapmaz. Fixed-width/fixed-offset parsing yapan kod, kullanıcı kontrollü bir alanın uzunluğunu doğru sınırlamazsa, sonraki tüm alanların pozisyonu kayabilir.
