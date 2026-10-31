### Brute Force için wordlist hazırlama 

```bash
awk 'length($0) >= 10 && /[a-z]/ && /[A-Z]/ && /[0-9]/' /opt/useful/seclists/.../rockyou.txt > custom_wordlist.txt 
```

**özel speclial characters istemiyorsak**

```bash
awk 'length($0) >= 12 && /[a-z]/ && /[A-Z]/ && /[0-9]/ && /^[a-zA-Z0-9]+$/' /usr/share/wordlists/rockyou.txt > custom_wordlist.txt
```


==Bu komutun içindeki mantığı şöyle parçalayabiliriz==

+ `grep -E '.{10,}'`: En az 10 karakter uzunluğundaki şifreleri seçer.
+ `grep '[a-z]'`: İçinde en az bir tane küçük harf olanları seçer.
+ `grep '[A-Z]'`: İçinde en az bir tane büyük harf olanları seçer.
+ `grep '[0-9]'`: İçinde en az bir tane rakam olanları seçer.
+ `>` işareti: Çıkan temiz listeyi custom_wordlist.txt adında yeni bir dosyaya kaydeder.
