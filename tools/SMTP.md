# SMPT (simple mail tranfer protokol)

**Basit Posta Aktarım Protokolü (SMTP), bir IP ağı üzerinden e-posta göndermek için kullanılan bir protokoldür.**
**SMTP genellikle, e-postaların alınıp gönderilmesini sağlayan `IMAP` veya `POP3` protokolleriyle birlikte kullanılır.**
### smtp ports
+ **Default:** `25`
+ **Yeni SMTP sunucuları** `587`
+ **Bazen** `465`
--- 

## IMAP&POP3 mailleri okumak için
[IMAP&POP3](https://github.com/ademsuslu/Hacking/blob/main/tools/imap%26pop3.md)


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
cd /opt/SMTPeek/target/release

 ./smtpeek -u /root/htb-academy/users.list -d inlanefreight.htb -c 5 10.129.203.7

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


## Kalide Python ile smpt listener açma


1. **openssl ile pem ouştur:**

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 1 -nodes \
  -subj "/CN=10.10.17.42" -addext "subjectAltName=IP:10.10.17.42"
```
**buradaki ip adresleri bizim local ip adresleri `/CN=my-local-vpn` `subjectAltName=IP:my-local-vpn`**

2. **listener aç**
**listener server codes**
```python
cat server.py 
import logging, os, ssl
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from aiosmtpd.smtp import AuthResult, LoginPassword

logging.basicConfig(level=logging.DEBUG)

HOST = "10.10.17.42"
PORT = 9999
USER = os.environ.get("SMTP_USER", "suslu7616")
PASS = os.environ.get("SMTP_PASS", "suslu7616")

def authenticator(server, session, envelope, mechanism, auth_data):
    if not isinstance(auth_data, LoginPassword):
        return AuthResult(success=False, handled=False)
    ok = (auth_data.login.decode() == USER and
          auth_data.password.decode() == PASS)
    return AuthResult(success=ok)

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("cert.pem", "key.pem")

controller = Controller(
    Debugging(),
    hostname=HOST,
    port=PORT,
    tls_context=ctx,
    require_starttls=False,
    authenticator=authenticator,
    auth_require_tls=False,
)
controller.start()
input("Çalışıyor. Durdurmak için Enter...")
controller.stop()

```


**listener**

```bash
python3 server.py
DEBUG:asyncio:Using selector: EpollSelector
INFO:mail.log:Available AUTH mechanisms: LOGIN(builtin) PLAIN(builtin)
INFO:mail.log:Peer: ('10.10.17.42', 51690)
INFO:mail.log:('10.10.17.42', 51690) handling connection
DEBUG:mail.log:('10.10.17.42', 51690) << b'220 suslusec Python SMTP 1.4.6'
INFO:mail.log:('10.10.17.42', 51690) EOF received
INFO:mail.log:('10.10.17.42', 51690) Connection lost during _handle_client()
Çalışıyor. Durdurmak için Enter...INFO:mail.log:('10.10.17.42', 51690) connection lost
INFO:mail.log:Available AUTH mechanisms: LOGIN(builtin) PLAIN(builtin)
INFO:mail.log:Peer: ('10.13.37.14', 43402)
INFO:mail.log:('10.13.37.14', 43402) handling connection
DEBUG:mail.log:('10.13.37.14', 43402) << b'220 suslusec Python SMTP 1.4.6'
DEBUG:mail.log:_handle_client readline: b'ehlo [172.22.0.3]\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'ehlo [172.22.0.3]'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-suslusec'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-SIZE 33554432'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-8BITMIME'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-SMTPUTF8'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-STARTTLS'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250-AUTH LOGIN PLAIN'
DEBUG:mail.log:('10.13.37.14', 43402) << b'250 HELP'
DEBUG:mail.log:_handle_client readline: b'AUTH PLAIN ********\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'AUTH PLAIN ********'
DEBUG:mail.log:Using builtin auth_ hook for 'PLAIN'
DEBUG:mail.log:auth_PLAIN returned AuthResult(success=True, handled=True, message=None, auth_data=...)
WARNING:mail.log:Session.login_data is deprecated and will be removed in version 2.0
DEBUG:mail.log:('10.13.37.14', 43402) << b'235 2.7.0 Authentication successful'
DEBUG:mail.log:_handle_client readline: b'mail FROM:<no-reply@faradaysec.com> size=133\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'mail FROM:<no-reply@faradaysec.com> size=133'
INFO:mail.log:('10.13.37.14', 43402) sender: no-reply@faradaysec.com
DEBUG:mail.log:('10.13.37.14', 43402) << b'250 OK'
DEBUG:mail.log:_handle_client readline: b'rcpt TO:<vamomanao@faradaysec.com>\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'rcpt TO:<vamomanao@faradaysec.com>'
INFO:mail.log:('10.13.37.14', 43402) recip: vamomanao@faradaysec.com
DEBUG:mail.log:('10.13.37.14', 43402) << b'250 OK'
DEBUG:mail.log:_handle_client readline: b'data\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'data'
DEBUG:mail.log:('10.13.37.14', 43402) << b'354 End data with <CR><LF>.<CR><LF>'
DEBUG:mail.log:DATA readline: b'Subject: Minus qui autem volu\r\n'
DEBUG:mail.log:DATA readline: b'\r\n'
DEBUG:mail.log:DATA readline: b'An event was reported at Barnie:\r\n'
DEBUG:mail.log:DATA readline: b'Quas quidem labore d\r\n'
DEBUG:mail.log:DATA readline: b'Here is your gift FARADAY{ehlo_@nd_w3lcom3!}\r\n'
DEBUG:mail.log:DATA readline: b'.\r\n'
---------- MESSAGE FOLLOWS ----------
mail options: ['SIZE=133']

Subject: Minus qui autem volu
X-Peer: ('10.13.37.14', 43402)

An event was reported at Barnie:
Quas quidem labore d
Here is your gift FARADAY{ehlo_@nd_w3lcom3!}
------------ END MESSAGE ------------
DEBUG:mail.log:('10.13.37.14', 43402) << b'250 OK'
DEBUG:mail.log:_handle_client readline: b'quit\r\n'
INFO:mail.log:('10.13.37.14', 43402) >> b'quit'
DEBUG:mail.log:('10.13.37.14', 43402) << b'221 Bye'
INFO:mail.log:('10.13.37.14', 43402) connection lost
INFO:mail.log:('10.13.37.14', 43402) Connection lost during _handle_client()


```
3. **serveri çalıştır**

```bash
python3 server.py
```


