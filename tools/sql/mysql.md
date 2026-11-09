# MySQL

+ **Port:** `3306`


## Default Configration

```bash
sudo apt install mysql-server -y
cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep -v "#" | sed -r '/^\s*$/d'

[client]
port        = 3306
socket      = /var/run/mysqld/mysqld.sock

[mysqld_safe]
pid-file    = /var/run/mysqld/mysqld.pid
socket      = /var/run/mysqld/mysqld.sock
nice        = 0

[mysqld]
skip-host-cache
skip-name-resolve
user        = mysql
pid-file    = /var/run/mysqld/mysqld.pid
socket      = /var/run/mysqld/mysqld.sock
port        = 3306
basedir     = /usr
datadir     = /var/lib/mysql
tmpdir      = /tmp
lc-messages-dir = /usr/share/mysql
explicit_defaults_for_timestamp

symbolic-links=0

!includedir /etc/mysql/conf.d/
```


## Dangerius Settings

| Settings | Description |
| ----------- | ----------- |
| `user` | MySQL hizmetinin hangi kullanıcıya sahip olacağı ayarlar. |
| `password` | MySQL kullanıcısının şifresini ayarlar. | 
| `admin_address` | İdari ağ arayüzünde TCP / IP bağlantılarını dinlemek için IP adresi. | 
| `debug` | Bu değişken mevcut hata ayıklama ayarlarını gösterir | 
| `sql_warnings` | Bu değişken, tek sıralı INSERT beyanlarının uyarılar meydana gelirse bir bilgi dizisi üretip üretmediğini kontrol eder. | 
| `secure_file_priv` | Bu değişken, veri ithalatı ve ihracat işlemlerinin etkisini sınırlamak için kullanılır. | 

---



## enumeration

```bash
sudo nmap 10.129.14.128 -sV -sC -p3306 --script mysql*
```

## connection
```bash
mysql -u root -pP4SSw0rd -h 10.129.14.128
```

## bağlantı sonrası commands

**databaseleri görme;**
```bash
show databases;
```
**version Öğrenme**

```bash
select version();
```


**database kullanma/seçme**

```bash
use mysql;
```


**seçlen dbdeki tabloları görme**


```bash
show tables;
```
**tablo içindeki bütün verileri görme**


```bash
select * from users;
```

### MySQL sunucusu için en önemli veritabanları
+ **system schema** `sys` 
+ **Information Schema** `information_schema` 

#### sys

```bash
use sys;
show tables;  

+-----------------------------------------------+
| Tables_in_sys                                 |
+-----------------------------------------------+
| host_summary                                  |
| host_summary_by_file_io                       |
| host_summary_by_file_io_type                  |
| host_summary_by_stages                        |
| host_summary_by_statement_latency             |
| host_summary_by_statement_type                |
| innodb_buffer_stats_by_schema                 |
| innodb_buffer_stats_by_table                  |
| innodb_lock_waits                             |
| io_by_thread_by_latency                       |
...SNIP...
| x$waits_global_by_latency                     |
+-----------------------------------------------+



select host, unique_users from host_summary;

```
