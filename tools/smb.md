# SMB Protokolü ve Enum4Linux Kullanımı

## SMB Protokolü Nedir?
SMB (Server Message Block) protokolü, TCP/IP üzerinde çalışan bir istek ve yanıt (request-response) protokolüdür.

## Enum4Linux Kullanımı
Enum4Linux aracının temel kullanım sözdizimi:

```sh
enum4linux [seçenekler] [IP]
```

### Kullanılabilir Seçenekler

| TAG  | FONKSİYON |
|------|------------|
| `-U` | Kullanıcı listesini al |
| `-M` | Makine listesini al |
| `-N` | Ad listesini dök ( -U ve -M'den farklıdır) |
| `-S` | Paylaşılan dizinleri listele |
| `-P` | Parola politikası bilgilerini al |
| `-G` | Grup ve üye listesini al |
| `-a` | Yukarıdaki tüm işlemleri yap (tam temel enumarasyon) |

## Örnek Tarama Sonucu
Bir tarama sonucunda aşağıdaki bilgileri elde edebiliriz:

```
Sharename       Type      Comment
---------       ----      -------
netlogon        Disk      Network Logon Service
profiles        Disk      Users profiles
print$          Disk      Printer Drivers
IPC$            IPC       IPC Service (polosmb server (Samba, Ubuntu))
```

Eğer bu bilgileri bulduysak, bir sonraki adım olarak SMB istemcisine bağlanabiliriz:

```sh
smbclient //[IP]/[SHARE]
```

Bağlanma için kullanılan temel etiketler:
- `-U [kullanıcı_adı]` : Kullanıcı adı belirtmek için kullanılır.
- `-p [port]` : Bağlanılacak portu belirtmek için kullanılır.

## SMB İstemcisi Kullanarak Dosya Alma
Suit kullanıcısından "secret" paylaşım dizinine erişim:

```sh
smbclient //10.10.10.2/secret -U suit -p 445
```

### SMB Client İçinde Bulunan Dosyayı Okuma
```sh
> more dosya_adı
```

### SMB Client İçinde Bulunan Dosyayı İndirme
```sh
> get dosya_adı
```

