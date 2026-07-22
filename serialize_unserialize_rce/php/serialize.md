# Serialized 


**Serialized Format — `O:7:"Profile":2:{s:8:"username";s:5:"guest";s:5:"theme";s:5:"light";}` Nedir?**


**serialize()**, bir PHP değişkenini/objesini metin haline getirir ki saklanabilsin/iletilebilsin. Format okunabilir ve her parçanın bir anlamı var. Şu örneği harf harf sökelim:

`O:7:"Profile":2:{s:8:"username";s:5:"guest";s:5:"theme";s:5:"light";}`


| Parça   |    Anlamı      
|---------|-------------
| O | Object (nesne) geliyor
|:7:| Sınıf adı 7 karakter uzunluğunda
| "Profile" |Sınıfın adı: `Profile`
|:2: | Nesnede 2 property var


**daha sonra objenin içi**
`{s:8:"username";s:5:"guest";s:5:"theme";s:5:"light";}`


**burada verilen herşeyin uzunlugu ve type belirtiliyor**

`{s:8:"username";s:5:"guest";s:5:"theme";s:5:"light";}`

`s:8:username` => string + 8 karakterden oluşuyor + (username) 8 karakter
`s:5:guest` => string + 5 karakterden oluşuyor + (username=guest) 5 karakter

**types**
| Kod | Tip               | Örnek                              |
|-----|-------------------|------------------------------------|
| s   | string            | s:5:"guest" → 5 harfli "guest"     |
| i   | integer           | i:42; → 42 sayısı                  |
| b   | boolean           | b:1; → true, b:0; → false          |
| d   | double (ondalık)  | d:3.14;                            |
| a   | array (dizi)      | a:2:{...} → 2 elemanlı dizi        |
| O   | object            | O:7:"Profile":2:{...}              |
| N   | null              | N;                                 |


# Tespit (Detection) vs Sömürü (Exploitation)

Parmak izleri (bir değer görünce tanı):

| Gördüğün          | Ne demek                           |
|-------------------|------------------------------------|
|  O: veya a:2:{ (bazen base64/URL-encoded)            |  **PHP** serialized   |
|  base64'te rO0AB veya hex AC ED 00 05        | **Java** serialized   |
|  base64'te gASV veya gAN       | **Python** pickle   |


# Sömürü (Exploitation)

Parmak izleri (bir değer görünce tanı):



Tespit ettikten sonra:
1. **Magic method'ları bul** — `__destruct`, `__wakeup`, `__toString` (deserialize'da otomatik tetiklenenler)
2. **Gadget bul** — o magic method'ların içinde işe yarar bir işlem var mı? (senin lab'da `file_put_contents` → dosya yaz)
3. **Payload kur** — gadget'ı kötüye kullanacak objeyi serialize et (senin `LogWriter`'ın)
4. Gönder ve tetikle (senin yaptığın)


## Magic Methodlar

PHP'de **iki alt çizgi (__) ile başlayan**, senin elle çağırmadığın **ama belirli olaylarda PHP'nin otomatik çağırdığı** özel metodlardır. Deserialization için önemli olanlar:

| Magic Method          |  Ne zaman OTOMATİK tetiklenir |
|-----------------------|-------------------------------|
|  __construct()        | Obje **new** ile oluşturulurken|
|  __wakeup()           | Obje **unserialize()** ile canlandırılırken|
|  __destruct()         | Obje yok edilirken (script biterken / bellekten silinirken)|
|  __toString()         | Obje bir **string** gibi kullanılırken (echo, string birleştirme...)|

En kritik gerçek:` unserialize()` objeyi kurarken `__construct`'ı ÇALIŞTIRMAZ ama `__wakeup`'ı çalıştırır, ve obje ölürken `__destruct`'ı çalıştırır. İşte saldırganın kapısı bu ikisi.




