# snmpwalk

```bash
snmpwalk -v2c -c public banksmarter.hsm 
```

Parametre | Anlamı ve Ne Yaptığı
---|---
`snmpwalk` | SNMP ağacında dolaşan (walk) bir istemci aracıdır. Bir OID'den (nesne tanımlayıcısı) başlayarak altındaki **tüm** dalları ve değerleri sırayla okur. 
`-v2c` | SNMP protokolünün **2c** sürümünü kullanır. Bu sürüm şifreleme içermez ve kimlik doğrulaması yalnızca "community string" (topluluk anahtarı) adı verilen düz metin bir şifreye bağlıdır.
`-c public` | Community string olarak **"public"** değerini kullanır. Bu, SNMP'nin varsayılan **salt-okunur (read-only)** şifresidir. (Bir diğer yaygın olanı da `private`'dır).
`banksmarter.hsm` | Hedefin hostname'i (veya IP adresi). (HSM, Hardware Security Module anlamına gelebilir, ancak büyük ihtimalle bu hedefin özel bir adıdır).
