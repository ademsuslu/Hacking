curl ile istek atılırken
```bash  
curl  --path-as-is  http://example.com/../../etc/passwd
```
şuna dönüşür
```bash  
curl  --path-as-is  http://example.com/etc/passwd
```
curl ile post isteği atma;
```bash
curl -X POST -H "Content-Type: application/x-www-form-urlencoded"   -d "<?php get ?>" https://api.example.com/upload
```
