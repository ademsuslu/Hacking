#Time-Based
Zaman tabanlı kör SQL enjeksiyonu, yukarıdaki boolean tabanlı olana çok benzerdir, çünkü aynı istekler gönderilir,
ancak bu sefer sorgularınızın yanlış veya doğru olduğuna dair görsel bir gösterge yoktur. Bunun yerine, doğru bir sorguya ilişkin göstergeniz,
sorgunun tamamlanmasının aldığı zamana dayanır. 
Bu zaman gecikmesi,  UNION ifadesinin yanı sıra SLEEP(x) gibi yerleşik yöntemler kullanılarak tanıtılır .
SLEEP() yöntemi yalnızca başarılı bir UNION SELECT ifadesi üzerine yürütülür. 

Örneğin, bir tablodaki sütun sayısını belirlemeye çalışırken aşağıdaki sorguyu kullanırsınız:

```bash
https://website.thm/article?id=admin123' UNION SELECT SLEEP(5);--
```
bu işlemlere aşağıdaki gibi devam etmemiz gerekiyor

[Boolean_based](./Tryhackme_Blind-SQLi-Boolean_Based.md)
