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
