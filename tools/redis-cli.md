# Redis pentesting
-a : password
``` bash
redis-cli -h 10.10.137.125  -a 'B65Hx562F@ggAZ@F'
```
login olmuş isek
``` bash
KEYS *
```
example 
1) "authlist"
2) "marketlist"
3) "internal flag"
4) "tmp"
5) "int"

```bash
GET internal flag
```
Get çalışmaz ise alternative kullanımlar

```bash
get "authlist"
---
type "authlist"
---
lrange "authlist" 0 10
```
