***ffuf ile subdomain scan***
``` bash
ffuf -u "http://team.thm" -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -H 'Host: FUZZ.team.thm'
```
