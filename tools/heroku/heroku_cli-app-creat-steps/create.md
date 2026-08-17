```bash
heroku login
```
```bash
heroku create app-name
```
```bash
heroku buildpacks:set heroku/php --app APP-ISMI ( buildpack yanı yazılım dilini seçicez)
```

```bash
git init .
```

```bash
git branch -M main
```

# 2. Dosyaları ekle ve commit yap
```bash
git add .
```
```bash
git commit -m "Subdomain Takeover PoC - myprint.booking.com"
```

# 3. Deploy et (main branch ile)
```bash
git push heroku main
```
