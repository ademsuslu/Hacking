# encode with hex


## example
```bash
echo -n '-1 ORDER BY 1 -- -' | xxd -p | tr -d '\n' | sed 's/^/0x/'
```
### parçalanmış hali

- `echo -n 'hello` ekrana hello yazdır
  
  -  `-n` new line eklemesin
- `xxd -p` hexedecimale çevir
- ` tr -d '\n'` çıktıda oluşabilicek new line varsa siler
- `sed 's/^/0x/'` çıktının başına 0x ekler 
   \
  - MySQL'e "bu sayı değil, hexadecimal bir string" olduğunu söylemek için `0x` ekleniyor.



# decode hexedecimal from text

```bash
echo -n '64656e656d6564656e656d6532' | xxd -p -r
# denemedeneme2  
```
