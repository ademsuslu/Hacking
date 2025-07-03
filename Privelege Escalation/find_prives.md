# Linux `find` Komutları Rehberi

Bu belge, CTF ortamlarında ve sistem keşfi sırasında kullanabileceğiniz güçlü `find` komutlarının bir derlemesidir. Hataları bastırmak ve temiz çıktı almak için genellikle `2>/dev/null` kullanılır.

---

## 🔐 SUID Bitli Dosyaları Bul

SUID bitine sahip dosyalar, ayrıcalık yükseltme için potansiyel vektörlerdir:

```bash
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm /4000 2>/dev/null
find / -type f -perm -04000 -ls 2>/dev/null
```

---

## 👥 Belirli Grup Sahipliğine Göre Dosya Bul

Örneğin, "bugtracker" grubuna ait tüm dosyaları bulmak için:

```bash
find / -type f -group bugtracker 2>/dev/null
```

---

## ✍️ Yazılabilir Dizinleri Bul

Sistemde yazılabilir tüm dizinleri listelemek:

```bash
find / -writable -type d 2>/dev/null
```

---

## 📄 Belirli Dosya veya Dizinleri Bul

Geçerli dizinde veya tüm sistemde belirli adlara sahip dosya/dizinleri bulmak:

```bash
find . -name flag1.txt
find /home -name flag1.txt
find / -type d -name config
```

---

## 🧷 İzinlere Göre Dosya Arama

### 1. 777 (tam erişimli) dosyaları bul:
```bash
find / -type f -perm 0777
```

### 2. Tüm kullanıcılar tarafından çalıştırılabilir dosyalar:
```bash
find / -perm a=x
```

---

## 👤 Kullanıcıya Ait Dosyaları Bul

Örneğin "frank" kullanıcısına ait tüm dosyalar:

```bash
find /home -user frank
```

---

## ⏳ Zaman Bazlı Dosya Arama

### 1. Son 10 günde **değiştirilen** dosyalar:
```bash
find / -mtime -10
```

### 2. Son 10 günde **erişilen** dosyalar:
```bash
find / -atime -10
```

### 3. Son 60 dakika içinde **değiştirilen** dosyalar:
```bash
find / -cmin -60
```

### 4. Son 60 dakika içinde **erişilen** dosyalar:
```bash
find / -amin -60
```

---

## 📦 Boyuta Göre Dosya Arama

### 1. Tam olarak 50MB olan dosyalar:
```bash
find / -size 50M
```

### 2. 50MB'dan büyük dosyalar:
```bash
find / -size +50M
```

### 3. 50MB'dan küçük dosyalar:
```bash
find / -size -50M
```

---

## 🧩 Ekstra: Daha Temiz Çıktı için

Hataları bastırmak amacıyla komutların sonuna genellikle `2>/dev/null` eklenir.

Örnek:
```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

