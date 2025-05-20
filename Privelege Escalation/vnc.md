shell aldıkdan sonra 


```bash
ps -aux
```
output:
```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
vncuser   1234  0.5  2.1 123456 78900 ?        Sl   May20   5:30 /usr/bin/Xvnc :1 -geometry 1920x1080 -depth 24 -rfbauth /home/vncuser/.vnc/passwd -rfbport 5901
```

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
