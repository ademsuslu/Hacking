#ssh_write

```bash  
ssh-keygen -t rsa -b 2048 -f benim_priv_key
```
yukarıdaki code  bize özel 2 key oluşturur bu keyler;

- benim_priv_key
- benim_priv_key.pub

eğer buradaki benim_priv_key.pub  keyini hedef makinanın authorized_key.pub dosyasının içine yazarsak


normal yani oluşturduğu diğer my_priv_keyi kullanarak giriş yapabiliriz

buradaki jake hedef makinada kimin auth keyine yazdıysak odur.
```bash  
ssh jake@localhost -i benim_priv_key
```
