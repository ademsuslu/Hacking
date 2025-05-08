bu bize özel bir .pub uzantılı key oluşturur bu key

```bash  
ssh-keygen -t rsa -b 2048 -f benim_priv_key
```
bu keyi hedef makinanın authorized_key.pub dosyasının içine yazarsak
normal yani oluşturduğu diğer my_priv_keyi kullanarak giriş yapabiliriz
```bash  
ssh jake@localhost -i benim_priv_key
```
