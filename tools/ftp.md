# Ftp File Transfer Protokol



## TFTP 
**Giriş için kullanıcı bilgisine gerek duymaz**

### TFTP Commands

| Commands | Description |
| ----------- | ----------- |
| `connect` | Dosya aktarımları için uzak ana bilgisayarı (ve isteğe bağlı olarak bağlantı noktasını) ayarlar. |
| `get` | Uzak ana bilgisayardan yerel ana bilgisayara bir dosya veya dosya grubu aktarır. | 
| `put` | Yerel ana bilgisayardan uzak ana bilgisayara bir dosya veya dosya grubu aktarır. | 
| `quit` | tftp programından çıkar.. | 
| `status` | Geçerli aktarım modu (ascii veya ikili/binary), bağlantı durumu, zaman aşımı değeri ve benzeri bilgiler dahil olmak üzere tftp'nin o anki durumunu gösterir. | 
| `verbose` | Dosya aktarımı sırasında ek bilgiler görüntülenmesini sağlayan ayrıntılı (verbose) modu açar veya kapatır.| 



## vsFTPd

**`vsFTPd`'nin varsayılan yapılandırması `/etc/vsftpd.conf` dosyasında bulunur ve bazı ayarlar halihazırda varsayılan olarak tanımlanmıştır.**

**Example `vsFTPd` Config File**

``` bash
cat /etc/vsftpd.conf | grep -v "#"
```

| Setting | Description |
| ----------- | ----------- |
| `listen=NO` | inetd üzerinden mi, yoksa bağımsız bir artalan süreci (daemon) olarak mı çalıştırılsın? |
| `listen_ipv6=YES` | IPv6'da dinleyin? |
| `anonymous_enable=NO` | Anonymous access'e izin verilsinmi ? |
| `local_enable=YES` | Local Userleri kabul edilsinmi |
| `dirmessage_enable=YES` | Active Directory mesajları görünsünmü |
| `use_localtime=YES` |  Localdeki zamanmı görünsün? |
| `uxferlog_enable=YES` |  Yükeleme ve indirme logları açıkmı olsun |
| `connect_from_port_20=YES` | 20. porttan bağlanılsınmı? |
| `secure_chroot_dir=/var/run/vsftpd/empty` | boş dizin adına izin verilsinmi |
| `pam_service_name=vsftpd` | Bu dize, PAM hizmetinin veskün kullanacağının adıdır. |
| `rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem` | Son üç seçenek, SSL şifreli bağlantılar için kullanılacak RSA sertifikasının yerini belirtir. |
| `rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key` | Servise, şifreli bağlantılar (FTPS / TLS) kurarken kullanması gereken özel anahtarın nerede olduğunu söyler. |


### FTPUSERS

```bash
cat /etc/ftpusers

guest
john
kevin
```


#### Tehlikeli ayarlar

| Setting | Description |
| ----------- | ----------- |
| `anonymous_enable=YES`	| Anonim girişe izin verilsin mi? |
|`anon_upload_enable=YES`	| Anonim kullanıcıların dosya yüklemesine izin verilsin mi? |
|`anon_mkdir_write_enable=YES`|	Anonim kullanıcıların yeni dizinler oluşturmasına izin verilsin mi? |
`no_anon_password=YES`	| Anonim kullanıcılardan parola istenmesin mi? |
| `anon_root=/home/username/ftp` |	Anonim kullanıcılar için dizin. |
| `write_enable=YES` |	STOR, DELE, RNFR, RNTO, MKD, RMD, APPE ve SITE gibi FTP komutlarının kullanımına izin verilsin mi? |

##### Anonymouse login

```bash
ftp 10.129.14.136

Name (10.129.14.136:cry0l1t3): anonymous

230 welcome


ftp> ls -R


```

##### vsFTPd Detailed Output

```bash
ftp> debug
ftp> trace
ftp> trace
```
# vsftpd Ayarları ve Güvenlik Notları

## Ayarlar

| Setting | Description |
|---|---|
| `dirmessage_enable=YES` | Kullanıcı bir dizine ilk girdiğinde mesaj gösterilip gösterilmeyeceğini belirler. |
| `chown_uploads=YES` | Anonim olarak yüklenen dosyaların sahipliğinin değiştirilip değiştirilmeyeceğini belirler. |
| `chown_username=username` | Anonim yüklenen dosyaların sahibi olarak atanacak kullanıcıyı belirtir. |
| `local_enable=YES` | Sistemdeki yerel kullanıcıların FTP üzerinden giriş yapmasına izin verir. |
| `chroot_local_user=YES` | Yerel kullanıcıları kendi ana dizinlerine hapseder, böylece dosya sisteminin geri kalanına erişemezler. |
| `chroot_list_enable=YES` | `chroot_list_file` ile tanımlanan kullanıcı listesinin kullanılmasını etkinleştirir. Liste nasıl yorumlanır, `chroot_local_user` değerine bağlıdır: `chroot_local_user=YES` iken listedeki kullanıcılar hapsedilmez (istisna listesi), `chroot_local_user=NO` iken listedeki kullanıcılar hapsedilir. |
| `hide_ids=YES` | Dizin listelerindeki tüm kullanıcı ve grup bilgileri "ftp" olarak görüntülenecektir. |
| `ls_recurse_enable=YES` | Tekrarlanan listelerin kullanılmasına izin verir. |

##### Güvenlik Açısından Dikkat Edilecekler

- **`chroot_local_user=NO` ise** yerel kullanıcılar dosya sisteminde serbestçe gezinebilir. Bu durum yetkisiz dizinlere erişim ve bilgi sızıntısı riskini artırır.
- **`chroot_local_user=YES` ve `chroot_list_enable=YES` birlikte kullanıldığında** listedeki kullanıcılar hapsedilmez. Liste yanlış yönetilirse bu kullanıcılar dosya sisteminin geri kalanına erişebilir. Listenin kasıtlı ve minimum tutulması gerekir.
- **`chown_uploads=YES` ve `chown_username`** birlikte kullanıldığında anonim yüklemeler belirtilen kullanıcıya ait olur. Bu kullanıcının yetkilerine bağlı olarak yetki yükseltme riski doğabilir. Bu kullanıcının ayrıcalıklı olmadığından emin olun.
- Bu ayarların yanında `anonymous_enable`, `write_enable` ve `anon_upload_enable` değerlerine de bakılmalıdır. Bu satırlar tek başına değerlendirildiğinde risk tam olarak anlaşılmaz; birlikte okunmaları gerekir.

##### Download All Available Files

```bash
wget -m --no-passive ftp://anonymous:anonymous@10.129.14.136

```
##### Upload File

```bash
put testupload.txt 
```

## Nmap FTP Scripts


```bash
find / -type f -name ftp* 2>/dev/null | grep scripts

/usr/share/nmap/scripts/ftp-syst.nse
/usr/share/nmap/scripts/ftp-vsftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-vuln-cve2010-4221.nse
/usr/share/nmap/scripts/ftp-proftpd-backdoor.nse
/usr/share/nmap/scripts/ftp-bounce.nse
/usr/share/nmap/scripts/ftp-libopie.nse
/usr/share/nmap/scripts/ftp-anon.nse
/usr/share/nmap/scripts/ftp-brute.nse
```

```bash
sudo nmap -sV -p21 -sC -A 10.129.14.136
```

**scriptlerinin ağ üzerinden gönderdiği ve aldığı tüm verileri ekrana yazdırmasını sağlayan bir seçenektir. `--script-trace`**
```bash
sudo nmap -sV -p21 -sC -A 10.129.14.136 --script-trace

NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #3 [10.129.14.136:21] (timeout: 7000ms) EID 58
NSOCK INFO [11.4640s] nsock_read(): Read request from IOD #4 [10.129.14.136:21] (timeout: 11000ms) EID 66
NSE: TCP 10.10.14.4:54226 > 10.129.14.136:21 | CONNECT
NSE: TCP 10.10.14.4:54228 > 10.129.14.136:21 | CONNECT

```

```bash
sudo nmap -sV -p21 -sC -A 10.129.14.136
```


## Service Interaction

**netcat**
```bash
 nc -nv 10.129.14.136 21
```
**telnet**

```bash
telnet  10.129.14.136 21
```
**openssl**

```bash
openssl s_client -connect 10.129.14.136:21 -starttls ftp
```



## FTP bounce Attack

```bash
nmap -Pn -v -n -p80 -b anonymous:password@10.10.110.213 172.17.0.2
```
