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
curl -A user agent verme;
```bash
curl -X POST -A "User-Agent: Mozilla"   -d "<?php get ?>" https://api.example.com/upload
```

curl -H ile header verme;
```bash
curl -X POST -H "Content-Type:application/json" -H "Referer: example.com"    -d "<?php get ?>" https://api.example.com/upload
```

curl -k ssl sorgulama;
```bash
curl  -K  https://api.example.com/upload
```

curl -v verbose (detay) alma;
```bash
curl  -v  https://api.example.com/upload
```
