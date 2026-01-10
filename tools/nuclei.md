# sadece bir url test etme

```bash
nuclei -t /root/.local/nuclei-templates/http/vulnerabilities/generic/open-redirect-generic.yaml -u https://example.com -c 30
```
# birden fazla test
```bash
 cat all.txt | nuclei -t /root/.local/nuclei-templates/http/vulnerabilities/generic/open-redirect-generic.yaml
```
