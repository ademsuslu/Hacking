# Reverse Shell Yönetimi ve Sudo Kontrolü

### Reverse Shell'i Yönetme

1. **Reverse Shell Başlatma**:
   Eğer bir reverse shell açmak istiyorsanız, aşağıdaki komutu kullanabilirsiniz:
   ```bash
   python3 -c 'import pty; pty.spawn("/bin/bash")'
ctrl+z
stty raw -echo; fg; ls; export SHELL=/bin/bash; export TERM=screen; stty rows 38 columns 116; reset;
   
    ```

Shell Kapatılması Durumu: Eğer açtığınız reverse shell kapanırsa veya yanlışlıkla kapanırsa, yeni bir shell açmak için şu adımları izleyebilirsiniz:

İlk olarak, TERM ortam değişkenini ayarlayın:
   ```bash
       export TERM=xterm
 ```

Eğer TERM değişkenini geri almak isterseniz, aşağıdaki komutu kullanabilirsiniz:
```bash
unset TERM

```
Shell'in Yeniden Başlatılması: Eğer shell'iniz kapanırsa, aşağıdaki komutları çalıştırarak yeniden açabilirsiniz:
``` bash
stty raw -echo; fg
```

Her zaman kontrol etmeniz gereken ilk şey → yapmaktır
``` bash
sudo -l
```

Komut , geçerli kullanıcının sistemde ayrıcalıklarla sudo -lçalıştırmasına izin verilen komutların listesini görüntüler.

Her zaman kontrol etmeniz gereken env dosyasında key PWD => passwd bulunabilir
``` bash
env
```



