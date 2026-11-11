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



