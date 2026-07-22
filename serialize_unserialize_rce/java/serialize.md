 # Java mı? — Tanıma (en kritik beceri)


| Encoding | Nasıl görünür | Ne demek |
|---|---|---|
| Raw bytes | `AC ED 00 05` ile başlar (Hex view'da) | Java serialized object |
| Base64 | `rO0AB` ile başlar | `AC ED 00 05`'in base64'ü |
| Gzip+Base64 | `H4sIA` ile başlar | Sıkıştırılmış, decode et |
| Base64 (URL-safe) | `rO0AB` ama `+/` yerine `-_` | Aynı şey |

> **Ezber:** `rO0AB` gördüğün an → %100 Java. Bu senin "PHP'deki `O:8:`" karşılığın.
