# Farklı Hesap ile Program Çalıştırma (RunAs)

Örneğin, standart bir kullanıcı hesabıyla oturum açtığınızda, yönetici yetkisi gerektiren bir işlemi **RunAs** kullanarak yönetici hesabıyla çalıştırabilirsiniz.

---

## Kullanım Amaçları

### Güvenlik Amaçlı Kullanım
Günlük işlerinizde düşük yetkili bir hesap kullanıyorsanız, yönetici işlemleri için sürekli hesap değiştirmenize gerek kalmaz.

### Ağ Kaynaklarına Erişim
Farklı bir kullanıcı adı ve parolasıyla bir uygulama çalıştırarak, ağdaki paylaşımlı kaynaklara erişebilirsiniz.

---

## RunAs Nasıl Kullanılır?

### 1. Komut Satırı ile Kullanım
```bash
runas /user:KULLANICIADI "program_yolu"
```
örnek
```bash
runas /user:Administrator "cmd.exe"
```


2. /savecred ile Şifreyi Kaydetme
```bash
runas /user:KULLANICIADI /savecred "program_yolu"
```
Bu seçenek, parolayı bir kez girdikten sonra Windows'ta saklar.

Dikkat: Şifre kaydı güvenlik riski oluşturabilir, dikkatli kullanılmalıdır.

3. Grafik Arayüz ile Kullanım
Bir programın kısayoluna sağ tıklayıp "Farklı bir kullanıcı olarak çalıştır" seçeneğini kullanabilirsiniz.

(Not: Windows 10/11'de bazı sürümlerde bu seçenek gizli olabilir.)

Önemli Parametreler

Parametre	Açıklama
/user	Hangi kullanıcıyla çalıştırılacağını belirtir (Örn: DOMAIN\Kullanıcı).
/savecred	Kullanıcının kimlik bilgilerini kaydeder (dikkatli kullanılmalı).
/profile	Kullanıcının profilini yükler (varsayılan olarak etkindir).
/env	Mevcut ortam değişkenlerini kullanır.
/netonly	Kimlik bilgileri yalnızca ağ bağlantıları için kullanılır.
Örnek Senaryolar
Yönetici Yetkisiyle Not Defteri Açma
```bash

runas /user:Admin "notepad.exe"
```
Domain Kullanıcısıyla Excel Çalıştırma
```bash
runas /user:COMPANY\user1 "C:\Program Files\Microsoft Office\Excel.exe"
```
Ağ Paylaşımına Erişim
```bash
runas /user:NETWORK\user2 /netonly "explorer.exe"
```
Dikkat Edilmesi Gerekenler
Parola Güvenliği: /savecred kullanıyorsanız, bilgisayarınıza fiziksel erişimi olan biri bu yetkiyi kötüye kullanabilir.

UAC (Kullanıcı Hesabı Denetimi): RunAs, UAC ile tamamen aynı şey değildir. UAC, bir programın yükseltilmiş yetkilerle çalışmasını sağlarken, RunAs tamamen farklı bir kullanıcıyla oturum açar.

Windows Sürümleri: Bazı Windows sürümlerinde (örneğin Home sürümleri) runas komutu sınırlı çalışabilir.

