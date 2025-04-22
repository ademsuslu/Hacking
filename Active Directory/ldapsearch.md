# 🎯 LDAP Enumeration Script (HTB - Sauna Örneği)

Bu proje, Hack The Box (HTB) üzerindeki **Sauna** makinesi özelinde kullanılan basit bir `ldapsearch` komutunun script haline getirilmiş halidir. Bu script, LDAP üzerinden Active Directory (AD) bilgi toplama (enumeration) işlemini gerçekleştirmek için kullanılır.

---

## 🛠 Kullanılan Araçlar

- `ldapsearch`: Linux üzerinde LDAP dizinlerinden veri çekmek için kullanılan araçtır.
- Protokol: `LDAP v3`

---

## 🧠 Ne İşe Yarar?

- Anonim (kimlik doğrulama olmadan) LDAP sorgusu yapar.
- Kullanıcılar, gruplar ve servis hesapları gibi AD nesnelerini listeler.
- CTF ve Penetrasyon Testleri sırasında reconnaissance (bilgi toplama) için kullanılır.

---

## ⚙️ Nasıl Kullanılır?

### 1. Scripti çalıştırılabilir yap:

```bash
chmod +x ldap_enum.sh
```
2. Çalıştır:
```bash
./ldap_enum.sh
```
3. Alternatif olarak parametrelerle manuel çalıştırmak istersen:
```bash
ldapsearch -x -H ldap://10.129.80.101 -D '' -w '' -b "DC=SAUNA,DC=EGOTISTICAL-BANK,DC=LOCAL"
```
📂 Script İçeriği (ldap_enum.sh)
```bash
#!/bin/bash
```
# Active Directory LDAP Bilgi Toplama Scripti (HTB Sauna Örneği)

SERVER="10.129.80.101"
BASEDN="DC=SAUNA,DC=EGOTISTICAL-BANK,DC=LOCAL"

ldapsearch -x -H ldap://$SERVER -D '' -w '' -b "$BASEDN"
💡 Notlar
Bu script, anonim LDAP erişimi mümkün olan AD ortamlarında çalışır.

Eğer bind yani kullanıcı adı/şifre gerekliyse -D ve -w parametrelerine uygun bilgileri girmeniz gerekir.

Daha fazla bilgi için: man ldapsearch

