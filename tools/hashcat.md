# Hashcat ile hash passwd cracking
## hazır payloads

1. **Blowfish/bcrypt**

```bash
hashcat -m 3200 hash.txt rockyou.txt
```
2. **md5**

```bash
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

## önce formatını öğren

```bash
hashid jsabhsbasbsahbhasbhabshabhsbahsbabsah
# forexample output: SHA-1
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









