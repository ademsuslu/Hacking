# hashcat ile hash cracking


```bash
hashid jsabhsbasbsahbhasbhabshabhsbahsbabsah

# forexample output: SHA-1

```


```bash
echo 'jsabhsbasbsahbhasbhabshabhsbahsbabsah' > admin.hash
```

```bash
echo 'jsabhsbasbsahbhasbhabshabhsbahsbabsah' > admin.hash
```

## kırmak için hangi formati vereceksek öğrenelim


```bash
hashcat -h  | grep SHA

# burada formatı vericek mesela:
100 - SHA-1
1300 - SHA2-224
...
```

```bash
hashcat -m 100 admin.hash /usr/share/wordlists/rockyou.txt
```









