# httpx kurulum için
```bash 
wget https://github.com/projectdiscovery/httpx/releases/download/v1.6.9/httpx_1.6.9_linux_amd64.zip
unzip httpx_1.6.9_linux_amd64.zip
mv httpx /usr/bin/httpx-url
chmod +x /usr/bin/httpx-url
httpx-url -l domains.txt -o alive.txt
```
