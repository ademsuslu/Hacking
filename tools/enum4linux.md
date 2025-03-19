enum4linux, Linux sistemlerinde çalışan ve Windows sistemlerinde Samba/CIFS paylaşım noktalarını ve güvenlik açıklarını taramak için kullanılan bir betiktir. SMB protokolü üzerinden bilgi toplamak için kullanılan bu araç, Windows sistemlerinde kullanıcı hesapları, paylaşımlar, oturumlar ve grup bilgileri gibi verileri çekmeye yardımcı olur. Özellikle pentest ve güvenlik değerlendirmelerinde sıkça kullanılır.

Temel Kullanımlar
1. Tüm Bilgileri Listeleme (Varsayılan Tarama)
bash
Copy
Edit
enum4linux -a <hedef-ip>
Bu komut hedef sistemden tüm kullanılabilir bilgileri toplar.

2. Kullanıcıları Listeleme
bash
Copy
Edit
enum4linux -U <hedef-ip>
Hedef sistemdeki kullanıcı hesaplarını listeler.

3. Paylaşılan Dizinleri Listeleme
bash
Copy
Edit
enum4linux -S <hedef-ip>
SMB protokolü üzerinden paylaşılan dizinleri görüntüler.

4. Grup Bilgilerini Çekme
bash
Copy
Edit
enum4linux -G <hedef-ip>
Hedef sistemdeki grup bilgilerini gösterir.

5. OS ve Versiyon Bilgisi Toplama
bash
Copy
Edit
enum4linux -o <hedef-ip>
Hedef sistemin işletim sistemi ve versiyon bilgilerini çeker.

README.md (Raw Format)
Aşağıda GitHub’a ekleyebileceğin README.md dosyası için raw içerik bulunuyor:

plaintext
Copy
Edit
# Enum4linux Kullanım Kılavuzu

`enum4linux`, Windows sistemlerinde Samba/CIFS paylaşım noktalarını ve güvenlik açıklarını taramak için kullanılan bir Linux aracıdır. SMB protokolü üzerinden bilgi toplamak için kullanılır ve genellikle sızma testleri ve güvenlik değerlendirmelerinde tercih edilir.

## Kurulum
Enum4linux varsayılan olarak birçok Linux dağıtımında bulunur. Eğer sisteminizde yoksa, aşağıdaki komutla yükleyebilirsiniz:

```bash
sudo apt install enum4linux
Alternatif olarak, git ile doğrudan kaynak kodunu çekebilirsiniz:

bash
Copy
Edit
git clone https://github.com/portcullislabs/enum4linux.git
cd enum4linux
chmod +x enum4linux.pl
Kullanım
Aşağıda temel enum4linux kullanım komutları bulunmaktadır:

1. Tüm Bilgileri Listeleme
Tüm kullanıcı hesapları, paylaşılan dosyalar ve hizmetler dahil olmak üzere mümkün olan tüm bilgileri çekmek için:

bash
Copy
Edit
enum4linux -a <hedef-ip>
2. Kullanıcıları Listeleme
bash
Copy
Edit
enum4linux -U <hedef-ip>
Hedef sistemdeki kullanıcı hesaplarını görüntüler.

3. Paylaşılan Dizinleri Listeleme
bash
Copy
Edit
enum4linux -S <hedef-ip>
SMB protokolü üzerinden paylaşılan dizinleri görüntüler.

4. Grup Bilgilerini Çekme
bash
Copy
Edit
enum4linux -G <hedef-ip>
Hedef sistemdeki grup bilgilerini görüntüler.

5. OS ve Versiyon Bilgisi Toplama
bash
Copy
Edit
enum4linux -o <hedef-ip>
Hedef sistemin işletim sistemi ve versiyon bilgilerini çeker.

Örnek Kullanım
Aşağıdaki örneklerde, 192.168.1.10 IP adresine sahip bir hedefe yönelik sorgular gerçekleştirilmektedir:

bash
Copy
Edit
enum4linux -a 192.168.1.10
enum4linux -U 192.168.1.10
enum4linux -S 192.168.1.10
enum4linux -G 192.168.1.10
enum4linux -o 192.168.1.10
