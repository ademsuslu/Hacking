SMB protokoli tcp/ip olarak calısır req ve res protokolüdür , 


The syntax of Enum4Linux is nice and simple: "enum4linux [options] ip"

TAG            FUNCTION

-U             get userlist
-M             get machine list
-N             get namelist dump (different from -U and-M)
-S             get sharelist
-P             get password policy information
-G             get group and member list
-a             all of the above (full basic enumeration)

örnek bir tarama sonucunda aşağıdakilere erişimimiz var.

                                                                                                                                            
        Sharename       Type      Comment
        ---------       ----      -------
        netlogon        Disk      Network Logon Service
        profiles        Disk      Users profiles
        print$          Disk      Printer Drivers
        IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))

eğer bunları buluyorsak sıradaki adım şu olmalı
smbclient //[IP]/[SHARE]
Followed by the tags:
-U [name] : to specify the user
-p [port] : to specify the port

suit kullanıcısından secreti alma işlemi
```bash
smbclient //10.10.10.2/secret -U suit -p 445
```
smb client içine girdiğimizde buldugumuz bır text yada pdf vb dosyayı okuma 
```
> more dosya_name
```
