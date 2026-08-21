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
