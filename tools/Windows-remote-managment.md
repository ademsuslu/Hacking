# Windows Uzak Yönetim Protokolleri

Windows sunucuları Server Manager gibi araçlarla hem yerel hem de uzaktan yönetilebilir. Uzak yönetim, Windows Server 2016 ile birlikte Server Manager'da varsayılan olarak etkinleştirilir. Ana protokoller şunlardır:

- **RDP** (Remote Desktop Protocol), TCP 3389
- **WinRM** (Windows Remote Management), TCP 5985 ve 5986
- **WMI** (Windows Management Instrumentation), TCP 135 ve dinamik portlar

---

## 1. RDP (Remote Desktop Protocol)

RDP, Microsoft'un geliştirdiği ve Windows sistemlere grafik arayüzle uzaktan erişim sağlayan bir protokoldür. Uygulama katmanında çalışır, varsayılan olarak TCP 3389 üzerinden iletişim kurar.

**Güvenlik notları:**

- Windows Vista'dan beri RDP trafiği **TLS/SSL** ile şifrelenir. Ancak birçok sistemde sertifika kendinden imzalıdır (self-signed) ve istemci bunu uyarı olarak gösterir. Bu durum ortadaki adam (MITM) saldırısına zemin hazırlayabilir.
- **NLA** (Network Level Authentication) etkinse, kimlik doğrulama oturum açılmadan önce yapılır. Varsayılan olarak RDP'de NLA açık değildir, ancak Server Manager'da etkinleştirilebilir.
- Dış ağdan erişim için NAT ve port yönlendirmesi kullanılır. Bu yapılandırma yanlış yapılırsa servis internete doğrudan açık hale gelir.

### RDP Keşfi (Footprinting)

**Nmap ile servis ve şifreleme bilgisi:**

```bash
nmap -sV -sC 10.129.201.248 -p3389 --script rdp*
```

Bu tarama şunları gösterir:
- Güvenlik katmanı (Security layer)
- CredSSP (NLA) ve Early User Auth desteği
- İşletim sistemi, NetBIOS ve DNS bilgileri

**Paket izleme ile detaylı inceleme:**

```bash
nmap -sV -sC 10.129.201.248 -p3389 --packet-trace --disable-arp-ping -n
```

Bu komut paketlerin ayrıntısını gösterir. Örneğin RDP sunucusu `TerminalServerCookie` içeren bir istek alıp `mstshash=nmap` çerezi ile yanıt verir. Bu bilgilerle RDP sunucusu tehdit avcıları ve EDR (Endpoint Detection and Response) çözümleri tarafından da tespit edilebilir.

### RDP Güvenlik Kontrolü: rdp-sec-check

Perl ile yazılmış bir araçtır ve RDP sunucusunun el sıkışma (handshake) aşamasındaki güvenlik ayarlarını kimlik doğrulaması olmadan kontrol eder.

```bash
git clone https://github.com/CiscoCXSecurity/rdp-sec-check.git
cd rdp-sec-check
./rdp-sec-check.pl 10.129.201.248
```

Kontrol edilen başlıklar:
- **Protokol desteği:** PROTOCOL_RDP, PROTOCOL_SSL, PROTOCOL_HYBRID
- **Şifreleme seviyeleri:** NONE, 40BIT, 128BIT, 56BIT, FIPS

Örnek sonucta `PROTOCOL_HYBRID` (CredSSP/NLA) destekleniyor, ancak eski protokoller ve şifrelemeler kapalı görünüyor.

**Gerekli kurulum (CPAN):** Araç bazı Perl modüllerine ihtiyaç duyar. `sudo cpan` ile yapılandırmayı tamamladıktan sonra eksik modüller (örneğin `Encoding::BER`) `install` komutuyla eklenebilir.

### RDP Oturumu Başlatma

Linux'ta RDP istemcileri: `xfreerdp`, `rdesktop`, `Remmina`.

```bash
xfreerdp /u:cry0l1t3 /p:"P455w0rd!" /v:10.129.201.248
```

- `/u:` kullanıcı adı
- `/p:` parola
- `/v:` hedef IP adresi

İlk bağlantıda sunucunun sertifikası doğrulanamadığı için bir uyarı çıkar. Sertifika hedef sunucuya aitse `y` ile devam edilir. Bağlantı kurulunca sunucunun masaüstü yeni bir pencerede açılır.

---

## 2. WinRM (Windows Remote Management)

WinRM, Windows'un komut satırı üzerinden uzaktan yönetim sağlayan web tabanlı protokolüdür. **SOAP** kullanır ve **TCP 5985** (HTTP) ile **TCP 5986** (HTTPS) portlarında çalışır. Bazı eski kurulumlarda 80 ve 443 portları da kullanılmıştır.

**Güvenlik notları:**

- WinRM, PowerShell uzaktan oturumları ve komut çalıştırma için kullanılır. `Windows Server 2012` ile birlikte varsayılan olarak etkindir.
- Bir kullanıcı WinRM yetkisine sahipse, uzaktan tam komut çalıştırabilir. Bu nedenle kimlik bilgisi sızıntısı çok kritik olur.
- `Test-WsMan` cmdlet'i, hedefin WinRM'e erişilebilir olup olmadığını kontrol eder.

### WinRM Keşfi

```bash
nmap -sV -sC 10.129.201.248 -p5985,5986 --disable-arp-ping -n
```

Açık ve HTTP yanıtı veren bir WinRM servisi genellikle `Microsoft-HTTPAPI` olarak görünür.

### Evil-WinRM ile Bağlantı

```bash
evil-winrm -i 10.129.201.248 -u cry0l1t3 -p 'P455w0rD!'
```

Bağlandıktan sonra PowerShell komutları çalıştırabilirsiniz. Evil-WinRM dosya yükleme ve indirme gibi ek özellikler de sunar.

---

## 3. WMI (Windows Management Instrumentation)

WMI, Microsoft'un **CIM** (Common Information Model) ve **WBEM** (Web-Based Enterprise Management) standartlarına dayanan yönetim altyapısıdır. Donanım, işletim sistemi, süreçler, servisler ve kullanıcılar hakkında bilgi sağlar. Yönetim için PowerShell, VBScript veya WMIC konsolu kullanılabilir.

**Güvenlik notları:**

- WMI, bağlantıyı **TCP 135** (RPC Endpoint Mapper) üzerinden kurar, sonrasında dinamik portlar kullanılır.
- WMI, yerel ve uzak sistemde komut çalıştırmak için kullanılabildiğinden saldırganların yanal hareket (lateral movement) için tercih ettiği bir araçtır.

### WMI Keşfi

Bağlantı ilk olarak TCP 135 üzerinden kurulur. Bu portun açık olup olmadığını kontrol edin:

```bash
nmap -p135 10.129.201.248
```

### wmiexec.py ile Uzaktan Komut Çalıştırma

Impacket paketindeki `wmiexec.py` aracı, WMI üzerinden etkileşimli bir kabuk açar:

```bash
/usr/share/doc/python3-impacket/examples/wmiexec.py cry0l1t3:"P455w0rD!"@10.129.201.248 "hostname"
```

Çıktıda SMB sürümü ve hedef sistemin host adı görünür. Bu örnekte host adı `ILF-SQL-01` olarak döner.

---

## Özet Tablo

| Protokol | Port | Kullanım | Araç |
|---|---|---|---|
| RDP | TCP 3389 | Grafik arayüzle uzaktan masaüstü | `xfreerdp`, `rdesktop`, `Remmina`, `rdp-sec-check` |
| WinRM | TCP 5985 / 5986 | PowerShell ve komut satırı | `evil-winrm`, `Test-WsMan` |
| WMI | TCP 135 + dinamik | Yönetim ve komut çalıştırma | `wmiexec.py` (Impacket) |

## Genel Güvenlik Değerlendirmesi

- Bu üç servis açıksa, **kimlik bilgisi** (kullanıcı adı ve parola) elde edilmesi çoğunlukla tam erişimle sonuçlanır. Bu yüzden parola politikası ve hesap kilitleme ayarları kritiktir.
- Servislere yalnızca gerekli ağlardan erişim verilmelidir. Güvenlik duvarı kurallarıyla 3389, 5985, 5986 ve 135 portları internete kapatılmalıdır.
- RDP için NLA açık olmalı, sertifikalar güvenilir bir CA tarafından imzalanmalı ve eski protokoller devre dışı bırakılmalıdır.
- WinRM için yalnızca HTTPS (5986) kullanılmalı, HTTP (5985) kapatılmalıdır.
