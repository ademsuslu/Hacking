# satır başına yada sonuna birşeyler eklemek için kullanılır


## satır başına birşeyler ekleme

```bash
echo -n "welcome" | sed 's/^/john/'
```

## satır sonuna birşeyler ekleme

```bash
echo -n "welcome" | sed 's/$/john/'
```


+ `s` → substitute (değiştir)
+ `^` → satırın başlangıcı
+ `$` → satırın sonuna 
+ `john` → başlangıca hello ekle

