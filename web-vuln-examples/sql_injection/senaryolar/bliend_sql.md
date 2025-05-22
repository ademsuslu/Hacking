2 adet item ekledik ve duruma göre listeletmemiz gerekiyorki flagı veya istediğimiz bilgileri çekelim;

http://example.com/order?=(CASE WHEN (SELECT SUBSTRING(flag,1,1) FROM flag)="C" THEN title ELSE date END)

- eğer flagın 1. harfi C ise title durumuna göre listelenir  değil ise date durumuna göre listelenir.
- ve her doğru harf için SUBSTRING(flag,1,2) ====> "CT" , SUBSTRING(flag,1,3) ====> "CTF" şeklinde artar 
