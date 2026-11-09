# 

## SSH / OPENSSH

+ iki bilgisayarın standart bağlantı noktasında olası güvensiz bir ağ içinde şifreli ve doğrudan bir bağlantı kurmasını sağlar. 
+ **port** `TCP 22`
+ `SSH-2SSH` sürüm 2 olarak da bilinen , şifreleme, hız, istikrar ve güvenlikte `SSH` sürüm 1'den daha gelişmiş bir protokoldür. Örneğin, SSH-1Savunmasız MITMSaldırılar, oysa `SSH-2` değil.



## public host key

İlk adımda, `SSH` sunucusu ve istemcisi kendilerini birbirlerine doğrular. Sunucu gönderiyor public host keyMüşterinin sunucunun kimliğini doğrulamak için kullandığı istemciye. Sadece temas ilk kurulduğunda, üçüncü bir tarafın iki katılımcı arasında kendisini araya sokma ve böylece bağlantıyı engelleme riski vardır. A. host keyEşsiz bir kamu-özel olduğu için taklit edilemez key pairVe bir saldırgan, müşterinin güvenilir bir kaynağa karşı kamu anahtarını doğruladığını varsayarak, özel anahtarın imzasını ona erişmeden oluşturamaz.


## Default Configration


```bash

cat /etc/ssh/sshd_config  | grep -v "#" | sed -r '/^\s*$/d'

Include /etc/ssh/sshd_config.d/*.conf
ChallengeResponseAuthentication no
UsePAM yes
X11Forwarding yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem       sftp    /usr/lib/openssh/sftp-server
```


## Dangerius settings


| Ayar | Açıklama |
|---|---|
| `PasswordAuthentication yes` | Parola tabanlı kimlik doğrulamasına izin verir. |
| `PermitEmptyPasswords yes` | Boş parolaların kullanılmasına izin verir. |
| `PermitRootLogin yes` | Root kullanıcısının giriş yapmasına izin verir. |
| `Protocol 1` | Eski ve güvensiz bir şifreleme sürümünü kullanır. |
| `X11Forwarding yes` | GUI uygulamaları için X11 yönlendirmesine izin verir. |
| `AllowTcpForwarding yes` | TCP portlarının yönlendirilmesine izin verir. |
| `PermitTunnel yes` | Tünelleme yapılmasına izin verir. |
| `DebianBanner yes` | Giriş yapılırken belirli bir banner gösterir. |


### SSH-Audit


```bash
ssh-audit 10.129.14.132
```


**Change Authentication Method**
```bash
ssh -v cry0l1t3@10.129.14.132

OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config 
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive

```

**Potansiyel kaba kuvvet saldırıları için, SSH istemci seçeneği Tercihli Kimlik Doğrulamaları ile kimlik doğrulama yöntemini belirtebiliriz.**

```bash
ssh -v cry0l1t3@10.129.14.132 -o PreferredAuthentications=password



OpenSSH_8.2p1 Ubuntu-4ubuntu0.3, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /etc/ssh/ssh_config
...SNIP...
debug1: Authentications that can continue: publickey,password,keyboard-interactive
debug1: Next authentication method: password

cry0l1t3@10.129.14.132's password:
```
## Rsync (uzaktan dosya copyalama)

**default port** `873`


### scan rsync

```bash
sudo nmap -sV -p 873 127.0.0.1


PORT    STATE SERVICE VERSION
873/tcp open  rsync   (protocol version 31)
```

#### Probing for Accessible Shares

```bash

nc -nv 127.0.0.1 873

(UNKNOWN) [127.0.0.1] 873 (rsync) open
@RSYNCD: 31.0
@RSYNCD: 31.0
#list
dev             Dev Tools
@RSYNCD: EXIT
```
#### Enumerating an Open Share



```bash
rsync -av --list-only rsync://127.0.0.1/dev

receiving incremental file list
drwxr-xr-x             48 2022/09/19 09:43:10 .
-rw-r--r--              0 2022/09/19 09:34:50 build.sh
-rw-r--r--              0 2022/09/19 09:36:02 secrets.yaml
drwx------             54 2022/09/19 09:43:10 .ssh
```

Yukarıdaki çıktıdan, daha fazla araştırmak için aşağı çekmeye değer birkaç ilginç dosya görebiliriz. SSH tuşları içeren bir dizinin erişilebilir olduğunu da görebiliriz. Buradan, tüm dosyaları saldırı ev sahipimize komut `rsync -av rsync://127.0.0.1/dev` ile senkronize edebiliriz. Rsync, dosyaları aktarmak için SSH'yi kullanacak şekilde yapılandırılmışsa, standart olmayan bir bağlantı noktası SSH için kullanılıyorsa, komutlarımızı `-esh` bayrağını veya `-e "ssh -p2222"` içerecek şekilde değiştirebiliriz. Bu kılavuz, SSH üzerinde Rsync kullanmak için sözdizimi anlamak için yararlıdır.


#### R-Services


## R-Services Özeti

**R-services**, Unix sistemlerde uzaktan komut çalıştırma ve oturum açma için kullanılan eski servislerdir (`rlogin`, `rsh`, `rexec`, `rwho`, `rusers`). Güvenlik zayıflıkları nedeniyle günümüzde yerini SSH almıştır.

**Temel sorun:** Bu servisler kimlik doğrulamayı, uzak istemcinin bildirdiği bilgilere güvenerek yapar. Bu da yanlış yapılandırıldığında yetkisiz erişime yol açar.

**Güven dosyaları:**

| Dosya | Kapsam |
|---|---|
| `/etc/hosts.equiv` | Sistem genelinde güvenilen host ve kullanıcılar. |
| `.rhosts` | Kullanıcı bazında güvenilen host ve kullanıcılar. |

Bu dosyalarda `+` karakteri bir joker anlamına gelir ve herhangi bir host ya da kullanıcıya izin verir. Bu nedenle yanlış yapılandırılmış bir `+` girdisi, kimlik bilgisi olmadan erişime imkân tanır.

**Keşif:** R-services ilgili portlar 512, 513 ve 514 üzerinde çalışır. Bu portlar açıksa servislerin aktif olduğu anlaşılır.

**Kullanılan araçlar:**
- `rlogin`: Güvenilen hosttan oturum açmak için.
- `rwho`: Ağdaki oturum açmış kullanıcıları listelemek için.
- `rusers`: Uzak sistemdeki kullanıcıları görüntülemek için.

**Bug bounty ve pentest açısından:** `.rhosts` veya `hosts.equiv` dosyalarında `+` girdisi bulunması, ciddi bir yetkisiz erişim riskidir. R-services'in açık olması da bu sistemin eski ve güvensiz bir yapılandırmaya sahip olduğunu gösterir.
