# Terminalde Hash (Özet) ve Hex Komutları Kullanım Kılavuzu

Terminal üzerinde `md5sum`, `md5`, `xxd` ve `sha` ailesini kullanarak metinlerin hash değerlerini ve ham çıktılarını bu komutlarla inceleyebilirsiniz.

---

### 1. MD5 Kullanımı
MD5, 128-bitlik (32 karakter) hızlı bir özetleme algoritmasıdır.

* **Linux (`md5sum`):**
  ```bash
  echo -n "merhaba" | md5sum
  # Çıktı: 5d41402abc4b2a76b9719d911017c592  -
  ```
* **macOS (`md5`):**
  ```bash
  echo -n "merhaba" | md5
  # Çıktı: 5d41402abc4b2a76b9719d911017c592
  ```

---

### 2. SHA Ailesi (SHA-1, SHA-256, SHA-512)
SHA algoritmaları, MD5'e göre çok daha güvenlidir. Günümüzde özellikle SHA-256 ve SHA-512 standart olarak kabul edilir.

* **SHA-1 (160-bit / 40 karakter):** Günümüzde çakışma (collision) riski nedeniyle güvensiz kabul edilir.
  ```bash
  echo -n "merhaba" | sha1sum
  # Çıktı: baf34551cef335c97480b340a4ee007b4074718e
  ```
* **SHA-256 (256-bit / 64 karakter):** En yaygın kullanılan güvenli şifreleme özetidir.
  ```bash
  echo -n "merhaba" | sha256sum
  # Çıktı: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
  ```
* **SHA-512 (512-bit / 128 karakter):** Çok daha uzun ve kırılması neredeyse imkansız olan bir özet üretir.
  ```bash
  echo -n "merhaba" | sha512sum
  # Çıktı: 9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043
  ```

---

### 3. OpenSSL ile Genel Çözüm (Alternatif)
Sisteminizde `sha256sum` gibi özel komutlar yoksa, `openssl` aracı ile tüm hash türlerini tek çatı altında çalıştırabilirsiniz:

```bash
echo -n "merhaba" | openssl dgst -md5
echo -n "merhaba" | openssl dgst -sha256
echo -n "merhaba" | openssl dgst -sha512
```

---

### 4. `xxd` ile Hex Dump ve Ham Çıktı İnceleme
`xxd` komutu, verilerin doğrudan bellekteki ham (binary) karşılığını veya hex dökümünü görmemizi sağlar.

* **Düz metnin Hex karşılığını görmek:**
  ```bash
  echo -n "1" | xxd
  # Çıktı: 00000000: 31                                      1
  # (Not: "1" karakterinin ASCII/Hex karşılığı 31'dir)
  ```
* **Bir Hash'in ham (binary) çıktısını Hex'e dökmek:**
  ```bash
  echo -n "merhaba" | md5sum | xxd
  ```
