# AWS IAM Misconfiguration Avı — Pentest Notları

> **Ana fikir:** AWS'de saldırganlar genelde zero-day aramaz. IAM izinlerindeki yanlış yapılandırmaları (misconfiguration) arar. AWS çok granüler izin verdiği için tek bir hatalı `Action`/`Resource` tanımı tüm ortamı ele geçirmeye yeter.

---

## 0. Başlangıç: Assume Breach

Senaryo: düşük yetkili bir kullanıcının access key'ini bir yerde buldun (örn. GitHub, `.env`, S3 bucket, log). Hedef → **admin olmak** veya **kalıcılık sağlamak**.

İlk iş: kim olduğunu ve neye yetkin olduğunu çıkarmak.

```bash
# 1. Kimliği doğrula
aws sts get-caller-identity

# 2. Kendi kullanıcı bilgin
aws iam get-user

# 3. Sana bağlı policy'leri listele
aws iam list-attached-user-policies --user-name <USER>
aws iam list-user-policies --user-name <USER>          # inline policy'ler
aws iam list-groups-for-user --user-name <USER>        # grup üzerinden gelen izinler

# 4. Policy içeriğini oku
aws iam get-user-policy --user-name <USER> --policy-name <NAME>
aws iam get-policy-version --policy-arn <ARN> --version-id <vX>
```

---

## 1. Privilege Escalation (Yetki Yükseltme)

Aranan tehlikeli izinler:

| İzin | Neden tehlikeli |
|------|-----------------|
| `iam:PutUserPolicy` | Kendine inline policy yazıp `AdministratorAccess` verirsin |
| `iam:AttachUserPolicy` | Kendine hazır admin policy'sini bağlarsın |
| `iam:CreateAccessKey` | Başka (yüksek yetkili) kullanıcı için key üretip onun kimliğine geçersin |
| `iam:CreatePolicyVersion` | Mevcut policy'ye admin sürüm ekleyip default yaparsın |
| `iam:UpdateAssumeRolePolicy` | Bir rolün güven politikasını değiştirip kendine assume ettirirsin |

**Dikkat:** `iam:Get*` ve `iam:List*` gibi masum görünen bir izin listesinin arasına `iam:PutUserPolicy` gizlenmiş olabilir. Policy'yi satır satır oku.

```bash
# PutUserPolicy ile kendine admin ver
aws iam put-user-policy --user-name <USER> \
  --policy-name esc --policy-document \
  '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}'
```

---

## 2. Lateral Movement — `iam:PassRole`

Direkt yukarı çıkamıyorsan yana kay. `iam:PassRole`, bir IAM rolünü bir AWS servisine (EC2, Lambda, ECS...) "geçirmene" izin verir.

**Saldırı zinciri:** `ec2:RunInstances` + `iam:PassRole` (admin bir role) varsa:
1. Admin rolünü bir EC2 instance'a bağlayıp instance'ı başlat
2. Instance'a gir → IMDS'ten (metadata) admin credential'larını çek
3. Admin yetkisiyle devam et

```bash
# Instance içinden metadata'dan credential çekme (IMDSv1)
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<ROLE_NAME>
```

> `PassRole` yalnız EC2 için değil — Lambda, Glue, CloudFormation, SageMaker gibi servislerde de zincirlenebilir.

---

## 3. Persistence (Kalıcılık)

Hesabı ele geçirince orada kalmak istersin.

- `iam:CreateAccessKey` + `Resource: user/*` → admin kullanıcı için **ikinci** bir secret key üret. Şifre değişmediği için CloudTrail yoksa fark edilmez.
- Bir IAM kullanıcının aynı anda **en fazla 2 aktif key**'i olabilir → ikincisini kendine ayır.
- Alternatif kalıcılık: yeni IAM user oluşturma, login profile ekleme, role trust policy değiştirme.

```bash
aws iam create-access-key --user-name <ADMIN_USER>
```

---

## 4. Wildcard Avı (En Kritik İpucu)

JSON policy'lerde **wildcard** ara — genelde en büyük hata burada:

| Kalıp | Anlamı |
|-------|--------|
| `"Action": "*"` | O resource üzerinde **her şeyi** yapabilir |
| `"Action": "iam:*"` | Tüm kimlik yapısı üzerinde tam kontrol |
| `"Resource": "*"` | İzin tüm kaynaklara uygulanır |
| `"Action": "s3:*"` | Tüm bucket'lara tam erişim |

`iam:*` + `Resource: *` = **FullIAMControl** → felaket senaryosu. O key'i bulan kişi ortamın kimlik yapısının tamamına sahiptir.

---

## 5. Otomasyon Araçları

Manuel enumeration yorucu olursa:

- **enumerate-iam** → mevcut key'in hangi izinlere sahip olduğunu brute-force ile çıkarır
- **Pacu** → AWS exploitation framework; escalation modülleri hazır (`iam__privesc_scan`)
- **ScoutSuite / Prowler** → geniş misconfig taraması
- **cloudsplaining** → indirilen policy'lerdeki tehlikeli izinleri raporlar

```bash
# Pacu privesc taraması
pacu > run iam__enum_permissions
pacu > run iam__privesc_scan
```

---

## ⚠️ Saha / Scope Uyarısı

- Bu adımlar **sadece kapsam (scope) AWS/IAM testine açıksa** denenir. Program kurallarını (policy) mutlaka önce oku.
- `PutUserPolicy`, `CreateAccessKey` gibi adımlar **aktif değişiklik** yapar → yetkin olmayan bir hesapta bunları çalıştırmak doğrudan izinsiz erişim/hasar sayılır.
- Bug bounty'de genelde önce **kanıt (PoC)** yeterli: `sts get-caller-identity` + izin listesini göstermek çoğu zaman escalation'ı fiilen yapmadan raporlanabilir. Gereksiz yıkıcı adımdan kaçın.
- Her adımı loglamayı unutma; rapor yazarken hangi izinle neyi kanıtladığın net olmalı.

---

## Hızlı Checklist

- [ ] `get-caller-identity` ile kimlik doğrulandı mı?
- [ ] Attached + inline + grup policy'leri çekildi mi?
- [ ] `PutUserPolicy` / `AttachUserPolicy` var mı?
- [ ] `CreateAccessKey` başka kullanıcılara mı işaret ediyor?
- [ ] `PassRole` + compute (`ec2:RunInstances` / `lambda`) kombinasyonu var mı?
- [ ] `iam:*`, `*`, `Resource: *` wildcard'ları var mı?
- [ ] Bulgular scope içinde mi? Aktif adım öncesi kural kontrolü yapıldı mı?