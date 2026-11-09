# Simple Network Management Protocol (SNMP)

**ağ cihazlarını izlemek için oluşturuldu**

**default ports**
+ `161`
+ `162`

## DEFAULT CONFIGRATION

<details>
<summary>SNP Daemon Config</summary>

```bash
cat /etc/snmp/snmpd.conf | grep -v "#" | sed -r '/^\s*$/d'

sysLocation    Sitting on the Dock of the Bay
sysContact     Me <me@example.org>
sysServices    72
master  agentx
agentaddress  127.0.0.1,[::1]
view   systemonly  included   .1.3.6.1.2.1.1
view   systemonly  included   .1.3.6.1.2.1.25.1
rocommunity  public default -V systemonly
rocommunity6 public default -V systemonly
rouser authPrivUser authpriv -V systemonly
```

</details>


## Dangerius settings


| setting | Description |
| ----------- | ----------- |
| `rwuser noauth` | **Kimlik doğrulama olmadan tam OID ağacına erişim sağlar.** |
| `rwcommunity <community string> <IPv4 address>` | **Taleplerin nereden gönderildiğine bakılmaksızın tam OID ağacına erişim sağlar.** |
| `rwcommunity6 <community string> <IPv6 address>` | **Hem de aynı erişim `rwcommunityIPv6` kullanma farkı ile.** |


## footprinting enumeration

### snmpwalk

``` bash
snmpwalk -v2c -c public 10.129.14.128
```


### snmpwalk

``` bash
snmpwalk -v2c -c public 10.129.14.128
```

### Communty stringi bulmak 

```bash
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.47.188
```

**buldugmuz bu string ile**

```bash
snmpwalk -v2c -c <bulunan_string> 10.129.47.188
```

**yada**

```bash
sudo apt install braa

braa <community string>@<IP>:.1.3.6.*   # Syntax

braa public@10.129.14.128:.1.3.6.*

10.129.14.128:20ms:.1.3.6.1.2.1.1.1.0:Linux htb 5.11.0-34-generic #36~20.04.1-Ubuntu SMP Fri Aug 27 08:06:32 UTC 2021 x86_64
10.129.14.128:20ms:.1.3.6.1.2.1.1.2.0:.1.3.6.1.4.1.8072.3.2.10
10.129.14.128:20ms:.1.3.6.1.2.1.1.3.0:548
10.129.14.128:20ms:.1.3.6.1.2.1.1.4.0:mrb3n@inlanefreight.htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.5.0:htb
10.129.14.128:20ms:.1.3.6.1.2.1.1.6.0:US
10.129.14.128:20ms:.1.3.6.1.2.1.1.7.0:78
...SNIP...
```
