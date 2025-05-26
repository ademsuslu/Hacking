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



