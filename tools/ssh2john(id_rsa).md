# ssh2john 

## şifreli bir id_rsa dosyasının hashini alıyoruz 

```bash
ssh2john id_rsa > id.hash
```
##  alınan hash dosyasını kırıyoruz 

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt id.hash
```
