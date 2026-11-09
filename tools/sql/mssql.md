# MSSQL


Microsoft'un SQL tabanlı ilişkisel veritabanı yönetim sistemidir. Son bölümde tartıştığımız MySQL'nin aksine MSSQL, kapalı kaynaktır ve başlangıçta Windows işletim sistemlerinde çalışacak şekilde yazılmıştır. Microsoft'un üzerinde çalışan uygulamalar oluştururken veritabanı yöneticileri ve geliştiriciler arasında popülerdir. NET çerçevesi, güçlü yerel desteği nedeniyle NET çerçeve. NET. MSSQL'nin Linux ve MacOS'ta çalışacak sürümleri var, ancak Windows'u çalıştıran hedefler konusunda MSSQL bulut sunucularına daha fazla rastlayacağız.

### Default Port

+ **MSSQL:** `1433`


## MSSQL Client

SQL Server Management Studio (SSMS) MSSQL yükleme paketi ile kurulabilen veya ayrı olarak indirilebilen ve yüklenebilen bir özellik olarak gelir. İlk yapılandırma ve veritabanlarının yöneticiler tarafından uzun vadeli yönetimi için sunucuya yaygın olarak yüklenir. SSMS'nin istemci tarafı uygulaması olduğu için, bir yöneticinin veya geliştiricinin veritabanını yönetmeyi planladığının herhangi bir sistemde kurulabileceğini ve kullanılabileceğini unutmayın. Sadece veritabanını barındıran sunucuda yok. Bu, veritabanına bağlanmamıza izin veren kayıtlı kimlik bilgilerine sahip SSMS ile savunmasız bir sisteme rastlayabileceğimiz anlamına gelir. Aşağıdaki resim SSMS'yi eylemde gösteriyor.


## MSSQL Veritabanı

MSSQL, bir hedef sunucuda barındırılabilecek tüm veritabanlarının yapısını anlamamıza yardımcı olabilecek varsayılan sistem veritabanlarına sahiptir. 
**İşte varsayılan veritabanları** ve her birinin kısa bir açıklaması:


| Default Veritabanı | Description |
|---|---|
| `master` | SQL sunucu örneği için tüm sistem bilgilerini izler |
| `model` | Oluşturulan her yeni veri tabanı için bir yapı görevi gören şablon veritabanı. Model veritabanında değiştirilen herhangi bir ayar, model veritabanındaki değişikliklerden sonra oluşturulan yeni veritabanına yansıyacaktır. |
| `msdb` | SQL Server Agent, işleri ve uyarıları planlamak için bu veritabanını kullanır. |
| `tempdb` | Geçici nesneleri saklayın |
| `resource` | SQL sunucusu ile dahil olan sistem nesneleri içeren yalnızca okunan veritabanı |


## NMAP MSSQL Senaryo Taraması


```bash
sudo nmap --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes --script-args mssql.instance-port=1433,mssql.username=sa,mssql.password=,mssql.instance-name=MSSQLSERVER -sV -p 1433 10.129.201.248

Starting Nmap 7.91 ( https://nmap.org ) at 2021-11-08 09:40 EST
Nmap scan report for 10.129.201.248
Host is up (0.15s latency).

PORT     STATE SERVICE  VERSION
1433/tcp open  ms-sql-s Microsoft SQL Server 2019 15.00.2000.00; RTM
| ms-sql-ntlm-info: 
|   Target_Name: SQL-01
|   NetBIOS_Domain_Name: SQL-01
|   NetBIOS_Computer_Name: SQL-01
|   DNS_Domain_Name: SQL-01
|   DNS_Computer_Name: SQL-01
|_  Product_Version: 10.0.17763

Host script results:
| ms-sql-dac: 
|_  Instance: MSSQLSERVER; DAC port: 1434 (connection failed)
| ms-sql-info: 
|   Windows server name: SQL-01
|   10.129.201.248\MSSQLSERVER: 
|     Instance name: MSSQLSERVER
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|     TCP port: 1433
|     Named pipe: \\10.129.201.248\pipe\sql\query
|_    Clustered: false

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.52 seconds

```

## MSSQL Ping Metasploit

```bash
msf6 auxiliary(scanner/mssql/mssql_ping) > set rhosts 10.129.201.248

rhosts => 10.129.201.248


msf6 auxiliary(scanner/mssql/mssql_ping) > run

[*] 10.129.201.248:       - SQL Server information for 10.129.201.248:
[+] 10.129.201.248:       -    ServerName      = SQL-01
[+] 10.129.201.248:       -    InstanceName    = MSSQLSERVER
[+] 10.129.201.248:       -    IsClustered     = No
[+] 10.129.201.248:       -    Version         = 15.0.2000.5
[+] 10.129.201.248:       -    tcp             = 1433
[+] 10.129.201.248:       -    np              = \\SQL-01\pipe\sql\query
[*] 10.129.201.248:       - Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

## Mssqlcient   ile bağlantı kurmak 

**HELP KULLAN**

```bash
impacket-mssqlclient Administrator@10.129.201.248 -windows-auth

SQL>  help

```

```bash
impacket-mssqlclient Administrator@10.129.201.248 -windows-auth



Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(SQL-01): Line 1: Changed database context to 'master'.
[*] INFO(SQL-01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (150 7208) 
[!] Press help for extra shell commands

SQL> select name from sys.databases

name                                                                                                                               

--------------------------------------------------------------------------------------

master                                                                                                                             

tempdb                                                                                                                             

model                                                                                                                              

msdb                                                                                                                               

Transactions


```
