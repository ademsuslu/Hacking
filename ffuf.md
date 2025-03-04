*** ffuf ile subdomain scan ***
. -fc 404,200 => sadece 404 ve 200 status kodlarına sahip olanları al
``` bash
└─# ffuf -u "http://team.thm" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -H 'Host: FUZZ.team.thm' -fc 404,200
```
