
# zip2john 

## şifreli bir backup.zip dosyasının hashini alıyoruz 

```bash
zip2john backup.zip > backup.hash
```
##  alınan hash dosyasını kırıyoruz 

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt backup.hash
```
