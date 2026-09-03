# faceted search & filter
Bu `query=:relevance:allCategories:menu-men-inco:isInPromo:true` bir faceted search parametresi.

**Ne Demek?**

```
:relevance          → Sırala: en alakalı olanlar ilk
:allCategories      → Kategori filterini açık tut
:menu-men-inco      → Sadece "menu-men-inco" kategorisini göster
:isInPromo          → Promosyon filtresi
:true               → Promosyondaki ürünler
```

**Backend'de Nasıl Çalışır?**

1. URL'den query parametresini al
   query = ":relevance:allCategories:menu-men-inco:isInPromo:true"

2. Colon'a göre split et (parse)
   [":relevance", "allCategories", "menu-men-inco", "isInPromo", "true"]

3. Key-value çiftleri oluştur
   {
     sort: "relevance",
     category: "allCategories:menu-men-inco",
     promo: "true"
   }

4. SQL Query Oluştur
   SELECT * FROM products 
   WHERE category = "menu-men-inco" 
   AND in_promo = true 
   ORDER BY relevance