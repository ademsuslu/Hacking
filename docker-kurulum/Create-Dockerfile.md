
# Örnek Dockerfile - Node.js uygulaması için

# 1. TEMEL IMAGE (ZORUNLU)
FROM node:18-alpine

# 2. ÇALIŞMA DİZİNİNİ BELİRLE
WORKDIR /app

# 3. BAĞIMLILIK DOSYALARINI KOPYALA (cache optimizasyonu için önce package.json)
COPY package*.json ./

# 4. BAĞIMLILIKLARI KUR (build-time)
RUN npm ci --only=production

# 5. UYGULAMA KODUNU KOPYALA
COPY . .

# 6. ORTAM DEĞİŞKENİ (isteğe bağlı)
ENV NODE_ENV=production
ENV PORT=8080

# 7. UYGULAMAYI DERLE (build)
RUN npm run build

# 8. HANGİ KULLANICI İLE ÇALIŞSIN (güvenlik)
USER node

# 9. HANGİ PORT DİNLENİYOR (dokümantasyon)
EXPOSE 8080

# 10. BAŞLANGIÇ KOMUTU (container çalıştığında)
CMD ["node", "dist/index.js"]

## tablo of Dockerfile

## Dockerfile Komutları Tablosu

| **Talimat** | **Açıklama** |
|-------------|--------------|
| **FROM** | Temel image'i belirtir. **ZORUNLU** ve ilk satırda olmalıdır. |
| **WORKDIR** | Çalışma dizinini ayarlar. Yoksa otomatik oluşturur. Sonraki tüm komutlar bu dizinde çalışır. |
| **COPY** | Dosya ve klasörleri host'tan container'a kopyalar. |
| **ADD** | COPY'ye ek olarak URL'den dosya indirebilir, tar.gz dosyalarını otomatik açar. **Genelde COPY tercih edilir.** |
| **RUN** | Build aşamasında çalıştırılan komutlar (bağımlılık kurma, derleme, vs.). Yeni bir image katmanı oluşturur. |
| **ENV** | Ortam değişkeni tanımlar. Container çalışırken bu değişkenler kullanılabilir. |
| **ARG** | Build sırasında `docker build --build-arg` ile dışarıdan değer alabilen değişkenler. |
| **EXPOSE** | Container'ın hangi portu dinlediğini **belgeler**. Portu AÇMAZ! `docker run -p` ile yönlendirme yapılmalıdır. |
| **USER** | Container'ın hangi kullanıcı ile çalışacağını belirler. Varsayılan root'tur. Güvenlik için önerilir. |
| **CMD** | Container başlatıldığında çalışacak varsayılan komut. **Dockerfile'da sadece 1 tane olabilir.** `docker run` ile override edilebilir. |
| **ENTRYPOINT** | Container başlatıldığında çalışacak ana komut. CMD'den farkı, `docker run` ile gelen argümanlar ENTRYPOINT'e eklenir, değiştirilmez. |
| **VOLUME** | Container'da kalıcı veri saklanacak dizinleri belirtir. |
| **LABEL** | Image'e metadata (versiyon, yazar, açıklama, vs.) eklemek için kullanılır. |
| **HEALTHCHECK** | Container'ın sağlık durumunu kontrol eden komut tanımlar. |
| **SHELL** | Varsayılan shell'i değiştirir (Linux'ta varsayılan `/bin/sh -c`). |

