# Dockerfile Notları

## Dockerfile nedir?
Image'i inşa eden **tarif**. Her satır bir adım (layer). `docker build -t isim .` ile çalışır.
Sonuç: `docker run` ile başlatılabilen bir image.

## Talimatlar (instructions)

| Talimat | İşi |
|---|---|
| **FROM** | Temel image (ZORUNLU, ilk satır) |
| **WORKDIR** | Çalışma dizini (kalıcı `cd`) |
| **COPY** | Senin makinenden → image'e dosya kopyalar |
| **ADD** | COPY gibi ama url indirir / tar açar (genelde COPY tercih edilir) |
| **RUN** | **Build sırasında** komut çalıştırır (kurulum, derleme) |
| **ENV** | Ortam değişkeni |
| **EXPOSE** | "Şu port dinleniyor" — sadece dokümantasyon, portu AÇMAZ |
| **USER** | Hangi kullanıcıyla çalışsın (varsayılan: root) |
| **ARG** | Build sırasında değişken |
| **CMD / ENTRYPOINT** | Container **başlarken** çalışacak komut |

## 🔑 En kritik ayrım: RUN vs CMD

| | Ne zaman | Örnek |
|---|---|---|
| **RUN** | Build sırasında (image'e pişer) | `npm run build` |
| **CMD** | Container başlarken (her `docker run`) | `node dist/index.js` |

## Örnek Dockerfile (Node.js — doğru sıra)

```dockerfile
FROM node:18-alpine            # 1. TEMEL IMAGE (zorunlu, ilk satır)

WORKDIR /app                   # 2. ÇALIŞMA DİZİNİ

COPY package*.json ./          # 3. önce bağımlılık dosyaları (cache optimizasyonu)

RUN npm ci                     # 4. TÜM bağımlılıkları kur (build araçları dev'de!)

COPY . .                       # 5. UYGULAMA KODUNU KOPYALA

RUN npm run build              # 6. DERLE (build araçları burada gerekli)

RUN npm prune --omit=dev       # 7. derleme bitti → dev bağımlılıklarını at (image küçülür)

ENV NODE_ENV=production        # 8. ÇALIŞMA-ZAMANI ortam değişkeni
ENV PORT=8080

USER node                      # 9. root DEĞİL, sınırlı kullanıcı (güvenlik)

EXPOSE 8080                    # 10. hangi port dinleniyor (dokümantasyon)

CMD ["node", "dist/index.js"]  # 11. container başlarken çalışacak komut

En yaygın hatalar
| **ARG** | Build sırasında değişken |
| **CMD / ENTRYPOINT** | Container **başlarken** çalışacak komut |

## 🔑 En kritik ayrım: RUN vs CMD

| | Ne zaman | Örnek |
|---|---|---|
| **RUN** | Build sırasında (image'e pişer) | `npm run build` |
| **CMD** | Container başlarken (her `docker run`) | `node dist/index.js` |

## Örnek Dockerfile (Node.js — doğru sıra)

```dockerfile
FROM node:18-alpine            # 1. TEMEL IMAGE (zorunlu, ilk satır)

WORKDIR /app                   # 2. ÇALIŞMA DİZİNİ

COPY package*.json ./          # 3. önce bağımlılık dosyaları (cache optimizasyonu)

RUN npm ci                     # 4. TÜM bağımlılıkları kur (build araçları dev'de!)

COPY . .                       # 5. UYGULAMA KODUNU KOPYALA

RUN npm run build              # 6. DERLE (build araçları burada gerekli)

RUN npm prune --omit=dev       # 7. derleme bitti → dev bağımlılıklarını at (image küçülür)

ENV NODE_ENV=production        # 8. ÇALIŞMA-ZAMANI ortam değişkeni
ENV PORT=8080

USER node                      # 9. root DEĞİL, sınırlı kullanıcı (güvenlik)

EXPOSE 8080                    # 10. hangi port dinleniyor (dokümantasyon)

CMD ["node", "dist/index.js"]  # 11. container başlarken çalışacak komut
```
