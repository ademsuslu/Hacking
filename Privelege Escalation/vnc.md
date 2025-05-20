shell aldıkdan sonra

eğer vnc açık ise localden yani kendi pcmizden terminalden 

- -L local
- -R remote
- -D dynamic

```bash
ssh -L 5901:127.0.0.1:5901 kullanıcı_adı@ip
```
yine kendi bilgisayarımızdan terminalden 

```bash
netstat -plnt 
```
eğer 5901 portunda bir şey açık ise 

yine kendi terminalimizden
```bash
vncviewer 127.0.0.1:5901 -passwd secret
```
bu şekilde bağlan şifreyi biliyorsak şifre ile yada -passwd dosya_name ile bağlanabiliriz.
