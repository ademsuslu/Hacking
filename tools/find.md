# Find 

- 1033 bytes in size
- not executable

```bash
find . -type f -size 1033c ! -executable
```


- owned by user bandit7
- owned by group bandit6
- 33 bytes in size
```bash
find . -type f -size 33c  -user bandit7 -group bandit6
```
