# SMB

## Genel Bakış

**SMB (Server Message Block)**, dosyalara, dizinlere ve yazıcılar, yönlendiriciler veya ağa açılmış arayüzler gibi diğer ağ kaynaklarına erişimi düzenleyen bir istemci-sunucu protokolüdür. TCP/IP üzerinde çalışan bir istek-yanıt (request-response) protokolüdür.

### Samba

Unix tabanlı işletim sistemleri için geliştirilmiş, SMB protokolünün alternatif bir sunucu uygulamasıdır.

---

## Keşif (Enumeration)

### Nmap ile SMB Script Taraması

```sh
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.103.254
```

### Servis Tespiti

```sh
sudo nmap 10.129.14.128 -sV -sC -p139,445
```

Örnek çıktı:

```
PORT    STATE SERVICE     VERSION
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
```

---

## Enum4Linux

### Temel Sözdizimi

```sh
enum4linux [seçenekler] [IP]
```

### Kullanılabilir Seçenekler

| Seçenek | Fonksiyon |
|---|---|
| `-U` | Kullanıcı listesini al |
| `-M` | Makine listesini al |
| `-N` | Ad listesini dök (`-U` ve `-M`'den farklıdır) |
| `-S` | Paylaşılan dizinleri listele |
| `-P` | Parola politikası bilgilerini al |
| `-G` | Grup ve üye listesini al |
| `-a` | Yukarıdaki tüm işlemleri yap (tam temel enumerasyon) |

### Örnek Çıktı

```
Sharename       Type      Comment
---------       ----      -------
netlogon        Disk      Network Logon Service
profiles        Disk      Users profiles
print$          Disk      Printer Drivers
IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))
```

---

## Paylaşımları Listeleme ve Bağlanma

Anonim (parolasız) olarak paylaşımları listelemek için:

```sh
smbclient -N -L //10.129.14.128
```

Belirli bir paylaşıma bağlanmak için:

```sh
smbclient //[IP]/[SHARE]
smbclient //10.10.10.2/secret -U suit -p 445
```

Kullanılan temel parametreler:

- `-N`: Parola sormadan bağlanır.
- `-U [kullanıcı_adı]`: Kullanıcı adı belirtir.
- `-p [port]`: Bağlanılacak portu belirtir.

Örnek çıktı:

```
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        home            Disk      INFREIGHT Samba
        dev             Disk      DEVenv
        notes           Disk      CheckIT
        IPC$            IPC       IPC Service (DEVSM)
```

---

## SMB Client İçinde Dosya İşlemleri

| Komut | Açıklama |
|---|---|
| `more dosya_adı` | Dosyayı istemci içinde okur. |
| `get dosya_adı` | Dosyayı yerel makineye indirir. |
| `!ls` | Yerel dizini listeler. |
| `!cat dosya_adı` | İndirilen yerel dosyayı okur. |

Örnek kullanım:

```
smb: \> get prep-prod.txt
smb: \> !ls
smb: \> !cat note.txt
```

---

## Samba Yapılandırması

### Varsayılan Yapılandırma

Yapılandırma dosyasını yorum satırları olmadan görüntülemek için:

```bash
cat /etc/samba/smb.conf | grep -v "#\|\;"
```

```ini
[global]
   workgroup = DEV.INFREIGHT.HTB
   server string = DEVSMB
   log file = /var/log/samba/log.%m
   max log size = 1000
   logging = file
   panic action = /usr/share/samba/panic-action %d

   server role = standalone server
   obey pam restrictions = yes
   unix password sync = yes

   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .

   pam password change = yes
   map to guest = bad user
   usershare allow guests = yes

[printers]
   comment = All Printers
   browseable = no
   path = /var/spool/samba
   printable = yes
   guest ok = no
   read only = yes
   create mask = 0700

[print$]
   comment = Printer Drivers
   path = /var/lib/samba/printers
   browseable = yes
   read only = yes
   guest ok = no
```

### Ayarlar

| Ayar | Açıklama |
|---|---|
| `[sharename]` | Ağ paylaşımının (share) adı. |
| `workgroup = WORKGROUP/DOMAIN` | İstemciler sorgu yaptığında görünecek çalışma grubu veya alan adı. |
| `path = /path/here/` | Kullanıcıya erişim verilecek dizin. |
| `server string = STRING` | Bağlantı başlatıldığında görünecek metin. |
| `unix password sync = yes` | UNIX parolasının SMB parolasıyla eşitlenip eşitlenmeyeceğini belirler. |
| `usershare allow guests = yes` | Kimlik doğrulaması yapmayan kullanıcıların tanımlı paylaşıma erişmesine izin verir. |
| `map to guest = bad user` | Kullanıcı girişi geçerli bir UNIX kullanıcısıyla eşleşmediğinde ne yapılacağını belirler. |
| `browseable = yes` | Bu paylaşımın kullanılabilir paylaşımlar listesinde gösterilip gösterilmeyeceğini belirler. |
| `guest ok = yes` | Parola istemeden bu servise bağlanmaya izin verir. |
| `read only = yes` | Kullanıcıların yalnızca dosyaları okuyabilmesini, değiştirememesini sağlar. |
| `create mask = 0700` | Yeni oluşturulan dosyalara atanacak izinleri belirler. `0700` ile yalnızca sahibi okuyabilir, yazabilir ve çalıştırabilir. |

### Tehlikeli Ayarlar

| Ayar | Açıklama |
|---|---|
| `browseable = yes` | Mevcut paylaşımın içindeki kullanılabilir paylaşımların listelenmesine izin verir. |
| `read only = no` | Dosya oluşturmaya ve değiştirmeye izin verir. |
| `writable = yes` | Kullanıcıların dosya oluşturmasına ve değiştirmesine izin verir. |
| `guest ok = yes` | Parola kullanmadan bu servise bağlanmaya izin verir. |
| `enable privileges = yes` | Belirli SID'lere atanmış ayrıcalıkların uygulanmasını sağlar. |
| `create mask = 0777` | Yeni oluşturulan dosyalara tüm kullanıcılar için tam izin verir. |
| `directory mask = 0777` | Yeni oluşturulan dizinlere tüm kullanıcılar için tam izin verir. |
| `logon script = script.sh` | Kullanıcı oturum açtığında çalıştırılacak scripti belirler. |
| `magic script = script.sh` | Script kapatıldığında çalıştırılacak scripti belirler. |
| `magic output = script.out` | Magic scriptin çıktısının nereye kaydedileceğini belirler. |

---

## Samba Servisini Yeniden Başlatma

```bash
sudo systemctl restart smbd
```

---

## Samba Durumu

`smbstatus` komutu ile aktif bağlantıları kontrol edebilirsiniz. Bu komut Samba sürümünü, istemcinin hangi sunucuya, hangi ana bilgisayardan ve hangi paylaşıma bağlı olduğunu gösterir. Bu bilgi, diğer kullanıcıların hâlâ erişebildiği bir alt ağa girildiğinde özellikle önemlidir.

---

## Güvenlik Notları

- **`guest ok = yes` ve `usershare allow guests = yes`** birlikte kullanıldığında paylaşım kimlik doğrulaması olmadan erişilebilir hale gelir.
- **`guest ok = yes` ve `writable = yes` birlikte** kullanıldığında kimlik doğrulaması olmadan dosya yazılabilir.
- **`create mask = 0777` ve `directory mask = 0777`** yeni dosya ve dizinleri herkes için okunabilir, yazılabilir ve çalıştırılabilir yapar.
- **`logon script` ve `magic script`** dosyaları yazılabilir bir konumdaysa, bir saldırgan bu scriptleri değiştirerek bir sonraki oturum açılışında veya script kapanışında kendi kodunu çalıştırabilir. Script dosyalarının ve dizinlerinin yazma izinleri kontrol edilmelidir.
- **`enable privileges = yes`** SID tabanlı ayrıcalıkları etkinleştirir. Bu ayrıcalıkların hangi kullanıcılara verildiği ayrıca incelenmelidir.
- **`read only = yes`** yazma riskini azaltır, ancak okuma yetkisi hassas dosyaların ifşasına yol açabilir.
