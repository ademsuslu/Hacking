.LFI Fuzzing;
```
-ic: Büyük/küçük harf duyarsız (ignore case).
-c: Renkli çıktı (color).
-mc parametresi: -mc 200,301,302
```
```bash
ffuf -u http://snoopy.htb/download?file=FUZZ -w /usr/share/wordlists/seclists/Fuzzing/LFI/LFI-etc-files-of-all-linux-packages.txt -ic -c -fs 0
```

*** ffuf ile subdomain scan ***
. -fc 404,200 => sadece 404 ve 200 status kodlarına sahip olanları al

``` bash
ffuf -u "http://team.thm" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -H 'Host: FUZZ.team.thm' -fc 404,200

# yada diğer payloads

ffuf -u "http://team.thm" -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million-5000.txt s-H 'Host: FUZZ.team.thm' -fc 404,200

```


. -fs 11366 => size boyutu sadece 11336 haricindekileri al
``` bash
 ffuf -u "http://team.thm" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -H 'Host: FUZZ.team.thm' -fs 11366
```
. parametre fuzzlama 
```bash
ffuf -u "http://snopy.htb/contact.php?FUZZ=whoami" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
```
