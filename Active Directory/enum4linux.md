# enum4linux

enum4linux, SMB protokolü kullanan makineler üzerinde bilgi toplamak için kullanılan bir araçtır. Windows makinelerindeki kullanıcılar, gruplar, paylaşımlar gibi bilgileri çekmek için kullanılır.

---

### 🔧 Kurulum

```bash
sudo apt install enum4linux
```

ya da

```bash
git clone https://github.com/portcullislabs/enum4linux.git
cd enum4linux
chmod +x enum4linux.pl
```

---

### 🔍 Kullanım

#### Tüm bilgileri listelemek için:

```bash
enum4linux -a <hedef-ip>
```

#### Kullanıcıları listelemek için:

```bash
enum4linux -U <hedef-ip>
```

#### Paylaşımları görmek için:

```bash
enum4linux -S <hedef-ip>
```

#### Grupları listelemek için:

```bash
enum4linux -G <hedef-ip>
```

#### İşletim sistemi bilgisi için:

```bash
enum4linux -o <hedef-ip>
```

---

### 💡 Örnek

```bash
enum4linux -a 192.168.1.10
```

---

### 📌 Not

- `enum4linux`, `rpcclient`, `smbclient`, `nmblookup` gibi araçları arkaplanda kullanır.
- Guest erişimi açıksa daha fazla bilgi elde edebilirsin.

---

### 🌐 Kaynak

[https://github.com/portcullislabs/enum4linux](https://github.com/portcullislabs/enum4linux)
