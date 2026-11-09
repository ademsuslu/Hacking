# SMPT (simple mail tranfer protokol)




**Basit Posta Aktarım Protokolü (SMTP), bir IP ağı üzerinden e-posta göndermek için kullanılan bir protokoldür.**
**SMTP genellikle, e-postaların alınıp gönderilmesini sağlayan `IMAP` veya `POP3` protokolleriyle birlikte kullanılır.**
### smtp ports
+ **Default:** `25`
+ **Yeni SMTP sunucuları** `587`
+ **Bazen** `465`
--- 

## IMAP&POP3 mailleri okumak için
[IMAP&POP3](https://github.com/ademsuslu/Hacking/edit/main/tools/imap¾pop3.md)


## Default Configration
<details>
<summary> Default Config
</summary>

```bash
cat /etc/postfix/main.cf | grep -v "#" | sed -r "/^\s*$/d"

smtpd_banner = ESMTP Server 
biff = no
append_dot_mydomain = no
readme_directory = no
compatibility_level = 2
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
myhostname = mail1.inlanefreight.htb
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
smtp_generic_maps = hash:/etc/postfix/generic
mydestination = $myhostname, localhost 
masquerade_domains = $myhostname
mynetworks = 127.0.0.0/8 10.129.0.0/16
mailbox_size_limit = 0
recipient_delimiter = +
smtp_bind_address = 0.0.0.0
inet_protocols = ipv4
smtpd_helo_restrictions = reject_invalid_hostname
home_mailbox = /home/postfix
```
</details>


| Komut | Açıklama |
|---|---|
| `AUTH PLAIN` | İstemciyi kimlik doğrulamak için kullanılan bir servis uzantısıdır. |
| `HELO` | İstemci bilgisayar adıyla oturum açar ve oturumu başlatır. |
| `MAIL FROM` | İstemci e-posta göndericisini belirtir. |
| `RCPT TO` | İstemci e-posta alıcısını belirtir. |
| `DATA` | İstemci e-postanın iletimini başlatır. |
| `RSET` | Başlatılan iletimi iptal eder, ancak istemci ile sunucu arasındaki bağlantıyı korur. |
| `VRFY` | Bir posta kutusunun mesaj iletimi için kullanılabilir olup olmadığını kontrol eder. |
| `EXPN` | Bu komutla bir posta kutusunun mesajlaşma için kullanılabilir olup olmadığını da kontrol eder. |
| `NOOP` | Zaman aşımı nedeniyle bağlantının kesilmesini önlemek için sunucudan yanıt ister. |
| `QUIT` | İstemci oturumu sonlandırır. |

**Güvenlik açısından dikkat edilecekler:**

- **`VRFY` ve `EXPN`** sunucunun geçerli kullanıcı adlarını doğrulamasına izin verir. Bu, kullanıcı numaralandırma (user enumeration) için kullanılabilir. Bu yüzden çoğu sunucuda kapatılması veya kısıtlanması gerekir.
- **`AUTH PLAIN`** kullanıcı adı ve parolayı Base64 ile kodlanmış olarak gönderir, şifrelemez. Bu nedenle bağlantının TLS ile korunmadığı durumlarda parola ağ üzerinden okunabilir.
- **`HELO` ile gönderilen istemci adı** sunucu tarafından doğrulanmaz. Sahte ad kullanılabilir, bu da kimlik doğrulamasını zayıflatır.


## Connect to smpt for telnet
SMTP sunucusuyla etkileşimde bulunmak için, SMTP sunucusuyla bir TCP bağlantısını başlatmak için telnet aracını kullanabiliriz.
Oturumu başlatmak için **HELO** yada **EHLO** kullanılır

```bash
telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 


HELO mail1.inlanefreight.htb

250 mail1.inlanefreight.htb


EHLO mail1

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING
```


##  Telnet - VRFY


**VRFY komutu, sistemdeki mevcut kullanıcıları listelemek için kullanılabilir. Ancak bu yöntem her zaman işe yaramaz. SMTP sunucusunun yapılandırmasına bağlı olarak, sunucu 252 kodunu döndürebilir ve sistemde aslında var olmayan bir kullanıcının varlığını onaylayabilir. Tüm SMTP yanıt kodlarının bir listesine bakılabilir**


```bash
telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server 

VRFY root

252 2.0.0 root


VRFY cry0l1t3

252 2.0.0 cry0l1t3


VRFY testuser

252 2.0.0 testuser


VRFY aaaaaaaaaaaaaaaaaaaaaaaaaaaa

252 2.0.0 aaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

## CONNECT with http method

```http
CONNECT 10.129.14.128:25 HTTP/1.0
```

## Send an Email

```bash
telnet 10.129.14.128 25

Trying 10.129.14.128...
Connected to 10.129.14.128.
Escape character is '^]'.
220 ESMTP Server


EHLO inlanefreight.htb

250-mail1.inlanefreight.htb
250-PIPELINING
250-SIZE 10240000
250-ETRN
250-ENHANCEDSTATUSCODES
250-8BITMIME
250-DSN
250-SMTPUTF8
250 CHUNKING


MAIL FROM: <cry0l1t3@inlanefreight.htb>

250 2.1.0 Ok


RCPT TO: <mrb3n@inlanefreight.htb> NOTIFY=success,failure

250 2.1.5 Ok


DATA

354 End data with <CR><LF>.<CR><LF>

From: <cry0l1t3@inlanefreight.htb>
To: <mrb3n@inlanefreight.htb>
Subject: DB
Date: Tue, 28 Sept 2021 16:32:51 +0200
Hey man, I am trying to access our XY-DB but the creds don't work. 
Did you make any changes there?
.

250 2.0.0 Ok: queued as 6E1CF1681AB


QUIT

221 2.0.0 Bye
Connection closed by foreign host.
```

## Dangerous Settings

### Open Relay Configuration

**Bu ayar ile bu SMTP sunucusu sahte e-postalar gönderebilir ve böylece birden fazla taraf arasındaki iletişimi başlatabilir. Başka bir saldırı olasılığı, e-postayı taklit etmek ve okumak olacaktır.**
```bash
mynetworks = 0.0.0.0/0
```

## smtp'de user enumeration

```bash
smtp-user-enum -M VRFY -U /usr/share/seclists/Usernames/Names/names.txt -t target-ip 
```

## Footprinting the Service

### nmap
```bash
sudo nmap 10.129.14.128 -sC -sV -p25

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-27 17:56 CEST
Nmap scan report for 10.129.14.128
Host is up (0.00025s latency).

PORT   STATE SERVICE VERSION
25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, CHUNKING, 
MAC Address: 00:00:00:00:00:00 (VMware)
```
### Nmap - Open Relay script

```bash
sudo nmap 10.129.14.128 -p25 --script smtp-open-relay -v

Starting Nmap 7.80 ( https://nmap.org ) at 2021-09-30 02:29 CEST
NSE: Loaded 1 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Initiating ARP Ping Scan at 02:29
Scanning 10.129.14.128 [1 port]
Completed ARP Ping Scan at 02:29, 0.06s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 02:29
Completed Parallel DNS resolution of 1 host. at 02:29, 0.03s elapsed
Initiating SYN Stealth Scan at 02:29
Scanning 10.129.14.128 [1 port]
Discovered open port 25/tcp on 10.129.14.128
Completed SYN Stealth Scan at 02:29, 0.06s elapsed (1 total ports)
NSE: Script scanning 10.129.14.128.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.07s elapsed
Nmap scan report for 10.129.14.128
Host is up (0.00020s latency).

PORT   STATE SERVICE
25/tcp open  smtp
| smtp-open-relay: Server is an open relay (16/16 tests)
|  MAIL FROM:<> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@nmap.scanme.org> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@ESMTP> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest%nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest%nmap.scanme.org">
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<"relaytest@nmap.scanme.org"@[10.129.14.128]>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<relaytest@nmap.scanme.org@ESMTP>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@[10.129.14.128]:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<@ESMTP:relaytest@nmap.scanme.org>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest>
|  MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@[10.129.14.128]>
|_ MAIL FROM:<antispam@[10.129.14.128]> -> RCPT TO:<nmap.scanme.org!relaytest@ESMTP>
MAC Address: 00:00:00:00:00:00 (VMware)

NSE: Script Post-scanning.
Initiating NSE at 02:29
Completed NSE at 02:29, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 0.48 seconds
           Raw packets sent: 2 (72B) | Rcvd: 2 (72B)
```


