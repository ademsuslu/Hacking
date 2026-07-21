# docker / container


**Docker servisi çalışıyor mu?**

``` bash
docker info
```

Bu komut ne yapıyor? Docker daemon'a bağlanıp sistem bilgisini (kaç container var, kaç image var, depolama vs.) soruyor. Yani aslında "motor çalışıyor mu?" testi.

İki ihtimal:

- Uzun bir bilgi listesi görürsen (Containers, Images, Server Version... gibi satırlar) → daemon çalışıyor, harika. ✅
- Şuna benzer bir hata görürsen:
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?


**Mevcut image ve container'ları görelim**

Ne yapıyor? İndirilmiş tüm kalıpları (tarifleri) listeler.

``` bash
docker images
```

**Tüm container'ları listele (duranlar dahil):**
Ne yapıyor? ps = container'ları listele. -a (all) = duranları da göster.

```bash
docker ps -a
```


# docker ayağa kaldırmak 

**İlk container'ı BİLİNÇLİ olarak çalıştıralım**

```bash
docker run hello-world
```
#### container oluştumu kontrol içi

```bash
docker ps -a
```

**Container'ın İÇİNE Girelim (en kritik beceri)**

- docker run → container ayağa kaldır
- `-it` → iki bayrağın birleşimi:
  - `-i` (interactive) = container'la etkileşimli kal, girdi gönderebil
  - `-t` (tty) = bana düzgün bir terminal ekranı ver
  - Yani `-it` = "içine gir ve klavyeyle konuşabileyim"
- ubuntu → hangi imaj? Ubuntu Linux imajı
- bash → container içinde hangi programı çalıştırayım? bash (komut satırı kabuğu)

```bash
docker run -it ubuntu bash
```


**Şimdi İzolasyonu Kanıtlayalım**

Bu container'ın Kali'nden gerçekten ayrı bir dünya olduğunu kendi gözünle gör. Container'ın içindeyken şu üç komutu sırayla çalıştır:

Ne yapıyor? Hangi işletim sistemi olduğunu söyler. Kali değil, Ubuntu yazdığını göreceksin — kanıt 1.

```bash
cat /etc/os-release
```

Ne yapıyor? Makine adını gösterir. 52f9722d5daf gibi bir şey çıkacak (Kali değil) — kanıt 2.

```bash
hostname
```


# Containerda app yazmak


1. Dockerfile oluşturuyoruz

    ``` cat Dockerfile
    # Temel imaj: içinde PHP 8.2 ve Apache web sunucusu hazır gelen resmi imaj
    FROM php:8.2-apache

    # src/ klasorundeki tum dosyalari Apache'nin web koku olan /var/www/html icine kopyala
    COPY src/ /var/www/html/

    # Lab amacli: web kokunu yazilabilir yap ki exploit ile dosya yazabilelim
    # (Gercek dunyada ASLA 777 verilmez! Sadece egitim icin.)
    RUN chmod -R 777 /var/www/html

    # Container'in 80 portunu disariya acacagimizi belirt (dokumantasyon amacli)
    EXPOSE 80
    ```

2. daha sonra hangi uygulamayı çalıştırcaksak kodlarını yazdıkdan sonra

    **src içinde kodlarımız olacak**

    ```bash
    ┌──(root㉿kali)-[~/deserial-labs/php]
    └─# ls
    Dockerfile  src
                                                                    
    ┌──(root㉿kali)-[~/deserial-labs/php]
    └─# ls src    
    index.php
    ```

3. docker çalıştırmak için `Dockerfile` dosyasının oldugun dizinde 

    ```bash
    docker build -t php-deserial-lab .
    ```


4. şimdi web sitesini ayağa kaldırmak için

    Komutu parçalayalım — her bayrak önemli:
    - `docker run` → container ayağa kaldır
    - `-d` (detached) → arka planda çalıştır. Web sunucusu sürekli açık kalmalı; terminalimizi kilitlemesin diye arka plana atıyoruz. (Hello-world'de -d yoktu, o yüzden çalışıp bitmişti; bu ise sürekli çalışacak.)
    - `-p 8080:80` → port yönlendirme. Kali'nin 8080 portunu, container'ın 80 portuna bağla. Yani tarayıcıda `localhost:8080` yazınca container'ın içindeki Apache'ye (port 80) ulaşırsın. Format: -p <kali-portu>:<container-portu>
    - `--name` php-lab → container'a php-lab adı ver (rastgele isim yerine, yönetmesi kolay olsun)
    - php-deserial-lab → hangi imajdan üretilecek

```bash
docker run -d -p 8080:80 --name php-lab php-deserial-lab

## output
dd358585d5c4f3f04ad5eb2845b3b5da22c84e43aa189faddcd38b0b18777a77

```

```bash
docker ps
   
## output
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS          PORTS                                     NAMES
dd358585d5c4   php-deserial-lab   "docker-php-entrypoi…"   12 seconds ago   Up 12 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   php-lab

```

## Çalışan Container'a Bağlanmak

hangi containere bağlammak istersek `Names` alıyoruz

```bash
 docker ps                                                                                     

CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                                     NAMES
dd358585d5c4   php-deserial-lab   "docker-php-entrypoi…"   9 minutes ago   Up 9 minutes   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   php-lab

```


ve buradan bağlanıyoruz

```bash
docker exec -it php-lab bash
```

## duran docker'ı yeniden başlatmak

```bash
docker start php-lab
```
