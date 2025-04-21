# CEH Sertifikası Hazırlık Yol Haritası

## Genel Bilgiler
- Süre: 12 Hafta
- Hedef: Certified Ethical Hacker (CEH) sertifikası almak
- Metod: Teorik + Pratik + Quiz
- Uygulama ortamları: TryHackMe, HackTheBox, Kali Linux

---
# CEH (Certified Ethical Hacker) Detaylı Konu Listesi

## 1. Siber Güvenlik ve Etik Hackerlık Temelleri
- CEH sertifikası nedir, amaçları nelerdir?
- Etik hacker tanımı ve türleri (White Hat, Black Hat, Gray Hat)
- Yasal sorumluluklar ve etik kurallar
- Siber güvenlik tehditleri ve trendleri
- Bilgi güvenliği üçgeni (CIA: Confidentiality, Integrity, Availability)

## 2. Ağ Temelleri ve Protokoller
- OSI Modeli ve katmanları
- TCP/IP modeli ve protokol yapısı
- IP adresleme, Subnetting, CIDR
- Yaygın protokoller: TCP, UDP, ICMP, DNS, HTTP, HTTPS, FTP, SSH, Telnet
- MAC adresi, ARP, RARP
- Portlar, socket'ler ve servislerin çalışma mantığı
- NAT, PAT ve VPN kavramları

## 3. Bilgi Toplama (Reconnaissance)
- Pasif bilgi toplama teknikleri
- Aktif bilgi toplama teknikleri
- Whois, nslookup, dig, theHarvester, recon-ng
- Google Dorking teknikleri
- Shodan ve Censys kullanımı
- Hedef sistem hakkında bilgi toplama süreçleri
- Metadata analizi

## 4. Tarama ve Nmap Kullanımı
- Hedef sistemlerin taranması
- Ping sweep, TCP/UDP taramaları
- Port ve servis taramaları
- Banner grabbing ve fingerprinting
- Nmap komutları ve script engine (NSE)
- Zafiyet tarama araçları: Nessus, OpenVAS, Nikto, Vulners

## 5. Sistem Hacking
- Kimlik doğrulama yöntemleri
- Parola kırma teknikleri: Brute force, Dictionary attack, Rainbow tables
- Hash algoritmaları: MD5, SHA-1, SHA-256
- Windows/Linux parola depolama yapıları
- Credential dumping (mimikatz)
- Privilege escalation yöntemleri
- Arka kapı oluşturma (backdoor)
- Antivirüs atlatma teknikleri (AV evasion)

## 6. Malware Tehditleri
- Malware türleri: Virüs, solucan, trojan, rootkit, ransomware, spyware, adware
- Malware bulaşma yöntemleri
- Command and Control (C2) yapısı
- Malware analiz yöntemleri: statik ve dinamik analiz
- Anti-debugging ve anti-VM teknikleri

## 7. Sniffing (Paket Dinleme)
- Paket analizi ve sniffer araçları (Wireshark, tcpdump)
- MITM (Man-In-The-Middle) saldırıları
- ARP spoofing / poisoning
- MAC flooding saldırıları
- DHCP saldırıları
- Sniffing koruma yöntemleri

## 8. Sosyal Mühendislik (Social Engineering)
- Sosyal mühendislik saldırı türleri: Phishing, Vishing, Smishing, Pretexting, Baiting
- E-posta spoofing, link spoofing
- Human firewall eğitimi
- SET (Social Engineering Toolkit) kullanımı
- Gerçek vakalar ve analizleri

## 9. Hizmet Dışı Bırakma Saldırıları (DoS/DDoS)
- DoS ve DDoS nedir? Farkları nelerdir?
- SYN flood, UDP flood, ICMP flood
- Botnet yapısı ve DDoS saldırıları
- LOIC/HOIC araçları
- DDoS koruma teknikleri ve CDN kullanımı

## 10. Oturum Kaçırma (Session Hijacking)
- TCP/IP oturumları nasıl çalışır?
- TCP handshake mantığı
- Session ID tahmini ve çalma yöntemleri
- Token hijacking
- ARP spoofing üzerinden oturum ele geçirme
- Oturum yönetimi güvenlik önlemleri

## 11. Web Uygulama Saldırıları
- OWASP Top 10 (özellikle şu başlıklar):
  - Injection (SQLi, Command Injection)
  - Cross-Site Scripting (XSS - Stored, Reflected, DOM)
  - Cross-Site Request Forgery (CSRF)
  - Security Misconfiguration
  - Broken Authentication
  - Sensitive Data Exposure
- Burp Suite ile zafiyet analizi
- Web uygulama firewall’ları (WAF) ve atlatma yöntemleri

## 12. Kablosuz Ağ Saldırıları
- WLAN yapısı ve protokoller
- WPA/WPA2/WPA3 güvenlik protokolleri
- Wi-Fi sniffing ve analiz (airmon-ng, airodump-ng)
- Wi-Fi şifre kırma (aircrack-ng, Reaver)
- Evil Twin saldırısı
- Rogue Access Point oluşturma

## 13. Mobil, IoT ve Bulut Güvenliği
- Android/iOS güvenlik farkları
- Mobil uygulama zafiyetleri (manifest dosyası, debug mode vs.)
- IoT cihazlardaki yaygın açıklıklar
- Bulut güvenlik tehditleri (AWS, Azure, GCP odaklı)
- Misconfigured cloud storage (S3 bucket örneği)
- Cloud pentesting araçları: ScoutSuite, Pacu

## 14. Güvenlik Duvarları, IDS/IPS ve Honeypotlar
- Güvenlik duvarı türleri (Stateful, Stateless, Proxy)
- IDS ve IPS nedir? Farkları nelerdir?
- Snort ve Suricata kullanımı
- Honeypot yapısı (low-interaction vs high-interaction)
- Kippo, Honeyd, Dionaea örnekleri

## 15. Kriptografi Temelleri
- Simetrik ve asimetrik şifreleme (AES, DES, RSA)
- Hashleme vs şifreleme farkı
- Dijital imzalar, sertifikalar ve PKI yapısı
- SSL/TLS protokolü
- Man-in-the-Middle ile şifreleme atlatma

## 16. CEH Sınavına Hazırlık ve Test Stratejileri
- Sınav formatı, soru tipleri
- Konu tekrarları ve hızlı notlar
- Pratik testler ve mock exam çözümü
- Sınavda zaman yönetimi ve ipuçları


---

## Kullanılacak Platformlar
- TryHackMe: [https://tryhackme.com/path/outline/ceh](https://tryhackme.com/path/outline/ceh)
- HackTheBox Academy
- VirtualBox + Kali Linux

## Kaynaklar
- CEH v12 Official Study Guide
- YouTube: HackerSploit, NetworkChuck
- Cybrary, INE Cybersecurity

## Haftalık Çalışma Planı
- Pazartesi: Konu çalış
- Salı: Pratik yap
- Çarşamba: Video izle
- Perşembe: Quiz çöz
- Cuma: THM/HTB modülü
- Hafta sonu: Tekrar + Not çıkar

---
