Windowsun env değerlerini verir
```bash
C:\>set
```
Çıktı:
```
Microsoft Windows [Version 10.0.17763.1821]
```
---
Windowsun versionunu verir

```bash
C:\>ver
```
Çıktı:
```
Microsoft Windows [Version 10.0.17763.1821]
```
---
systeminfo Komutu çalıştırarak sistem hakkında işletim sistemi bilgileri

```bash
C:\>systeminfo
```
Çıktı:
```
C:\>systeminfo

Host Name:                 WIN-SRV-2019
OS Name:                   Microsoft Windows Server 2019 Datacenter
OS Version:                10.0.17763 N/A Build 17763
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
[...]
```
---
System hakkında detaylıca bilgi verir .

```bash
C:\>systeminfo
```
Çıktı:
```
C:\>systeminfo

Host Name:                 WIN-SRV-2019
OS Name:                   Microsoft Windows Server 2019 Datacenter
OS Version:                10.0.17763 N/A Build 17763
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
[...]
```
---
Ağ yapılandırmanız hakkında daha fazla bilgi için de kullanabilirsiniz ipconfig /all. Aşağıdaki terminalde gösterildiği gibi, DNS sunucularımızı görüntüleyebilir ve DHCP'nin etkinleştirildiğini doğrulayabiliriz .

```bash
C:\>ipconfig /all
```
Çıktı:
```
C:\>ipconfig /all

Ethernet adapter Ethernet 3:

   Connection-specific DNS Suffix  . : eu-west-1.compute.internal
   Description . . . . . . . . . . . : Amazon Elastic Network Adapter
   Physical Address. . . . . . . . . : 02-B7-DF-1D-0D-99
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   Link-local IPv6 Address . . . . . : fe80::90df:4861:ba40:f2a8%4(Preferred) 
   IPv4 Address. . . . . . . . . . . : 10.10.230.237(Preferred) 
   Subnet Mask . . . . . . . . . . . : 255.255.0.0
   Lease Obtained. . . . . . . . . . : Wednesday, May 1, 2024 2:38:05 PM
   Lease Expires . . . . . . . . . . : Wednesday, May 1, 2024 4:08:07 PM
   Default Gateway . . . . . . . . . : 10.10.0.1
   DHCP Server . . . . . . . . . . . : 10.10.0.1
   DHCPv6 IAID . . . . . . . . . . . : 134353458
   DHCPv6 Client DUID. . . . . . . . : 00-01-00-01-27-E3-D1-2B-0E-F8-30-D0-72-3F
   DNS Servers . . . . . . . . . . . : 10.0.0.2
   NetBIOS over Tcpip. . . . . . . . : Enabled
```
---



