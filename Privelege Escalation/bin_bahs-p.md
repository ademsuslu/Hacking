örneğin bir sistemde herhangi bir kullanıcıya
/usr/bin/chmod +s /bin/bash yekisini verebiliyorsak 
gerek sistemi yeniden başlattıkdan sonra /bin/bash -p çalıştırdığımızda root olur 

detaylar


-p Parametresinin Anlamı
/bin/bash -p komutundaki -p parametresi, bash'in "privilege" (ayrıcalık) modunda çalışmasını sağlar. Kısaca:

Normalde: Bir setuid/setgid program çalıştırdığınızda, bash güvenlik nedeniyle efektif kullanıcı ID'nizi (UID) gerçek kullanıcı ID'nize düşürür.

-p ile: Bash bu güvenlik önlemini devre dışı bırakır ve efektif kullanıcı ID'nizi (root olarak) korur.

Senaryodaki Durum:
chmod +s /bin/bash ile bash'e setuid biti eklediniz (root olarak).

Artık /bin/bash root yetkileriyle çalışıyor.

bash -p komutuyla bu root yetkisini koruyarak tam yetkili bir shell elde ediyorsunuz.

Özet: -p olmazsa bash root yetkisini düşürür, -p ile root kalır. CTF'lerde privilege escalation için kritik bir
