## liste icindeki uzantiya gore satirlari silme

**satırın sonunda .svg,.png.. ile biten bütün satırları siler ve kalanları yeni_liste.txt dosyasına yazar**

```bash
grep -vE '\.(svg|png|jpeg|woff)$' tum_arsiv_linkleri.txt > yeni_liste.txt
```



+ `grep`: Metin içinde arama ve filtreleme yapar.
+ `-v`: Eşleşen satırları hariç tutar (yani siler/çıkarır).
+ `-E`: Birden fazla uzantıyı (VEYA mantığıyla) aramayı sağlar.
+ `'\.(svg|png|jpeg|woff)$'`: Satırın sonunda nokta ile başlayan bu uzantıları bulur.
+ `>`: Sonucu yeni bir dosyaya yazar


# grep ile belirli yerleri kesip alma


**bu listin içinden sadece winId= değerinden sonraki kısımları almak için**
```bash
cat tum_arsiv_linkleri2.txt | grep "winId"
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=11d7f882-05a4-436e-8815-68eaf7478c19
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=1625729c-e429-4dff-8e98-dfee73b1a38c
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=1b490d61-9907-4730-b758-56ad7d259340
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=246aff36-401a-417d-99c9-c8f3260e5de7
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=2c225794-a254-479d-9e72-87634bd70797
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=5c76346a-f96c-4df5-90b2-2ec1ac00b450
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=7517f083-b6d2-4dca-9edc-3658980b247e
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=9bc7cac4-41fe-4b6d-bac8-e397f51c3cbf
```

```bash
grep -oP 'winId=\K[^&]*' tum_arsiv_linkleri.txt
```
