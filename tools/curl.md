curl ile istek atılırken
```bash  
curl  --path-as-is  http://example.com/../../etc/passwd
```
şuna dönüşür
```bash  
curl  --path-as-is  http://example.com/etc/passwd
```
