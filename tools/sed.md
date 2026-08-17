# Satır başına yada sonuna birşeyler eklemek için kullanılır


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

## Bu, hacker kelimesini dosyanın ilk satırına ekler.

```bash
sed -i '1i hacker' wordlist.txt
```
+ burada `-i` değişebilir 1,2,3 yada istediğimiz satırda kullanabiliriz   

