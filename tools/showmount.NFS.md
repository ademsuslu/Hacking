#NFS 
# NFS Network File System `TCP/UDP 2049`

## Remote Procedure Call `TCP ve UDP 111`


### Default Configuration

<details>
<summary>
NFS Default Configration
</summary>

```bash
cat /etc/exports 

# /etc/exports: the access control list for filesystems which may be exported
#               to NFS clients.  See exports(5).
#
# Example for NFSv2 and NFSv3:
# /srv/homes       hostname1(rw,sync,no_subtree_check) hostname2(ro,sync,no_subtree_check)
#
# Example for NFSv4:
# /srv/nfs4        gss/krb5i(rw,sync,fsid=0,crossmnt,no_subtree_check)
# /srv/nfs4/homes  gss/krb5i(rw,sync,no_subtree_check)
```
</details>

**NFS Config Codları**

| Seçenek | Açıklama |
|---|---|
| `rw` | Okuma ve yazma izni verir. |
| `ro` | Yalnızca okuma izni verir. |
| `sync` | Senkron veri aktarımı yapar. (Biraz daha yavaş) |
| `async` | Asenkron veri aktarımı yapar. (Biraz daha hızlı) |
| `secure` | 1024 üzerindeki portların kullanılmasına izin vermez. |
| `insecure` | 1024 üzerindeki portların kullanılmasına izin verir. |
| `no_subtree_check` | Alt dizin ağacı kontrolünü devre dışı bırakır. |
| `root_squash` | Root UID/GID 0 olan dosyaların yetkisini anonim kullanıcının UID/GID değerine atar. Böylece `root` kullanıcısı NFS bağlamında dosyalara erişemez. |

**Güvenlik açısından dikkat edilecekler:**

### ExportFS

```bash
echo '/mnt/nfs  10.129.14.0/24(sync,no_subtree_check)' >> /etc/exports
systemctl restart nfs-kernel-server 
exportfs

/mnt/nfs        10.129.14.0/24
```
#### Dangerius Settings

| Seçenek | Açıklama |
|---|---|
| `rw` | Okuma ve yazma izni verir. |
| `insecure` | 1024 üzerindeki portların kullanılmasına izin verir. |
| `nohide` | Dışa aktarılan bir dizinin altına başka bir dosya sistemi bağlandıysa, bu dizin kendi `exports` girdisiyle ayrıca dışa aktarılır. |
| `no_root_squash` | Root tarafından oluşturulan tüm dosyalar UID/GID 0 ile saklanır. |

**Güvenlik açısından dikkat edilecekler:**

- **`no_root_squash`** uzaktan bağlanan root kullanıcısının sunucuda da root yetkisiyle dosya oluşturmasına ve değiştirmesine izin verir. Bug bounty'de öncelikli olarak raporlanması gereken bir yanlış yapılandırmadır.
- **`rw` ve `no_root_squash` birlikte** kullanıldığında yazma yetkisi olan bir saldırgan, root olarak SUID bir dosya oluşturabilir ve yerel yetki yükseltmeye zemin hazırlayabilir.
- **`insecure`** 1024 üzerindeki portlardan bağlantıya izin verir. Tek başına kritik değildir, ancak diğer zayıf ayarlarla birlikte saldırı yüzeyini genişletir.
- **`nohide`** ile birlikte, dışa aktarılan dizinin altındaki bağlı dosya sistemleri de ayrıca erişilebilir hale gelebilir. Bu, dizin hiyerarşisinde beklenmedik alanların açılmasına yol açabilir.

## Footprinting the Service

```bash
sudo nmap 10.129.14.128 -p111,2049 -sV -sC
```
**Script Tarama**
```bash
sudo nmap --script nfs* 10.129.14.128 -sV -p111,2049
```


## Targetin nfs paylaşımını görme

```bash
showmount -e 10.129.14.128

Export list for 10.129.14.128:
/mnt/nfs 10.129.14.0/24
```


## nfs Bağlanma


```bash
mkdir target-NFS
sudo mount -t nfs 10.129.14.128:/ ./target-NFS/ -o nolock
cd target-NFS
tree .

 .
└── mnt
    └── nfs
        ├── id_rsa
        ├── id_rsa.pub
        └── nfs.share

2 directories, 3 files
```

## Kullanıcı Adayları ve Grup Adlı İçerikleri Listeleyin

```bash
ls -l mnt/nfs/

total 16
-rw-r--r-- 1 cry0l1t3 cry0l1t3 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 cry0l1t3 cry0l1t3  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1 root     root     1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1 root     root      348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1 root     root        0 Sep 19 17:22 nfs.share
```

## UIDS ve GUID'li İçerikleri Listeleyin

```bash
ls -n mnt/nfs/

-rw-r--r-- 1 1000 1000 1872 Sep 25 00:55 cry0l1t3.priv
-rw-r--r-- 1 1000 1000  348 Sep 25 00:55 cry0l1t3.pub
-rw-r--r-- 1    0 1000 1221 Sep 19 18:21 backup.sh
-rw-r--r-- 1    0    0 1872 Sep 19 17:27 id_rsa
-rw-r--r-- 1    0    0  348 Sep 19 17:28 id_rsa.pub
-rw-r--r-- 1    0    0    0 Sep 19 17:22 nfs.share
```

## target makinanın paylaşımından cıkma

```bash
cd ..
umount ./target-NFS
```
### Açık portları 

+ 111
+ 635
+ 2049
+ 4045
+ 4049

## targette paylaşılanları gösterir 
```bash
showmount -e $TARGET_IP
```
örnek çıktı

```bash
Export list for $TARGET_IP:
/srv/nfs/onboarding *
```

## şimdi buna kendi bilgisayarımızdan bağlanıcaz 

```bash
mkdir -p /tmp/onboarding

sudo mount -t nfs $TARGET_IP:/srv/nfs/onboarding /tmp/onboarding -o ro
```
