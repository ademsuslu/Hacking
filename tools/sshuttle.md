# sshuttle

Bu aracın en güzel özelliği: **Proxychains kullanmana gerek kalmaması!** Proxychains ile Nmap atmak çok yavaştı ve `-sn` (ping) çalışmıyordu ya, `sshuttle` bunu çözüyor. Arka planda `iptables` kuralları yazarak sanki C makinesiyle aynı ağdaymışsın gibi doğrudan bağlantı kurmanı sağlıyor.

İşte not alman için görseldeki kodlar ve ne işe yaradıkları:

### 1. Kurulum (A Makinesinde)
```bash
sudo apt-get install sshuttle
```

### 2. Tüneli Başlatma (A Makinesinde)
```bash
sudo sshuttle -r ubuntu@10.129.202.64 172.16.5.0/23 -v
```
*   **`-r ubuntu@10.129.202.64`**: B (Pivot) makinesine SSH ile bağlan (Ubuntu).
*   **`172.16.5.0/23`**: C'nin bulunduğu iç ağı (hedef ağı) tünele dahil et.
*   **`-v`**: Ekranda neler olup bittiğini göster (verbose).

### 3. Test / Tarama (A Makinesinde)
```bash
sudo nmap -v -A -p 3389 172.16.5.19 -Pn
```
**Dikkat et:** Başında `proxychains` **YOK!** Çünkü `sshuttle` çalışırken arkada sisteme gerekli rotaları ekledi. Direkt Nmap atabiliyorsun, hem de çok hızlı.

*(Not: Görselin en altındaki Optional Exercise'te senden `sshuttle` kullanarak RDP ile C makinesine bağlanmanı istiyor. Tünel açıkken direkt `xfreerdp /v:172.16.5.19 ...` komutunu kullanabilirsin, proxychains'e gerek yok.)*
