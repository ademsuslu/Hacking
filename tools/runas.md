Farklı Hesap ile Program Çalıştırma

Örneğin, standart bir kullanıcı hesabıyla oturum açtığınızda, yönetici yetkisi gerektiren bir işlemi RunAs kullanarak yönetici hesabıyla çalıştırabilirsiniz.

Güvenlik Amaçlı Kullanım

Günlük işlerinizde düşük yetkili bir hesap kullanıyorsanız, yönetici işlemleri için sürekli hesap değiştirmenize gerek kalmaz.

Ağ Kaynaklarına Erişim

Farklı bir kullanıcı adı ve parolasıyla bir uygulama çalıştırarak, ağdaki paylaşımlı kaynaklara erişebilirsiniz.

RunAs Nasıl Kullanılır?
1. Komut Satırı ile Kullanım
cmd
runas /user:KULLANICIADI "program_yolu"
Örnek:

cmd
runas /user:Administrator "cmd.exe"
Bu komut çalıştırıldığında, belirtilen kullanıcının parolası sorulur ve komut istemi (cmd) o kullanıcı yetkileriyle açılır.

2. /savecred ile Şifreyi Kaydetme
cmd
runas /user:KULLANICIADI /savecred "program_yolu"
Bu seçenek, parolayı bir kez girdikten sonra Windows'ta saklar (güvenlik riski oluşturabilir, dikkatli kullanılmalıdır).

3. Grafik Arayüz ile Kullanım
Bir programın kısayoluna sağ tıklayıp "Farklı bir kullanıcı olarak çalıştır" seçeneğini kullanabilirsiniz (Windows 10/11'de bazı sürümlerde bu seçenek gizli olabilir).

Önemli Parametreler
Parametre	Açıklama
/user	Hangi kullanıcıyla çalıştırılacağını belirtir (Örn: DOMAIN\Kullanıcı).
/savecred	Kullanıcının kimlik bilgilerini kaydeder (dikkatli kullanılmalı).
/profile	Kullanıcının profilini yükler (varsayılan olarak etkindir).
/env	Mevcut ortam değişkenlerini kullanır.
/netonly	Kimlik bilgileri yalnızca ağ bağlantıları için kullanılır.
Örnek Senaryolar
Yönetici Yetkisiyle Not Defteri Açma

cmd
runas /user:Admin "notepad.exe"
Domain Kullanıcısıyla Excel Çalıştırma

cmd
runas /user:COMPANY\user1 "C:\Program Files\Microsoft Office\Excel.exe"
Ağ Paylaşımına Erişim

cmd
runas /user:NETWORK\user2 /netonly "explorer.exe"
Dikkat Edilmesi Gerekenler
Parola Güvenliği: /savecred kullanıyorsanız, bilgisayarınıza fiziksel erişimi olan biri bu yetkiyi kötüye kullanabilir.

UAC (Kullanıcı Hesabı Denetimi): RunAs, UAC ile tamamen aynı şey değildir. UAC, bir programın yükseltilmiş yetkilerle çalışmasını sağlarken, RunAs tamamen farklı bir kullanıcıyla oturum açar.

Windows Sürümleri: Bazı Windows sürümlerinde (örneğin Home sürümleri) runas komutu sınırlı çalışabilir.

RunAs, özellikle sistem yöneticileri ve geliştiriciler için güçlü bir araçtır, ancak yetki yönetiminde dikkatli olunmalıdır.
