# IAM Enumeration Cheat Sheet

## 1. List IAM Users

```bash
aws iam list-users
```

## 2. Get User Permissions

**a. List attached managed policies**

```bash
aws iam list-attached-user-policies --user-name [user-name]
```

**b. List inline policies**

```bash
aws iam list-attached-user-policies --user-name [user-name]
```

**c. Get inline policy details**

```bash
aws iam get-user-policy --user-name [user-name] --policy-name [policy-name]
```
## 3. List IAM Groups and Permissions


**a. List groups for a user**
```bash
aws iam list-groups-for-user --user-name [user-name]
```


**b. List group policies**

```bash
aws iam list-attached-group-policies --group-name [group-name]
aws iam list-group-policies --group-name [group-name]
```

**c. Get inline group policy details**

```bash
aws iam get-group-policy --group-name [group-name] --policy-name [policy-name]
```

## 4. List IAM Roles and Permissions

**a. List all roles**

```bash
aws iam list-roles
```

**b. Get role details (trust policy)**

```bash
aws iam get-role --role-name [role-name]
```


**c. List attached policies**

```bash
aws iam list-attached-role-policies --role-name [role-name]
```

**d. List inline policies**

```bash
aws iam list-role-policies --role-name [role-name]
```

**e. Get inline role policy details**

```bash
aws iam get-role-policy --role-name [role-name] --policy-name [policy-name]
```



## 5. Get and Decode Policy Documents


**a. Get a managed policy document (by ARN or name)**

```bash
aws iam get-policy --policy-arn [policy-arn]
aws iam get-policy-version --policy-arn [policy-arn] --version-id [version-id]
```

## 6. View Full IAM Snapshot

**a. Dump all IAM permissions (users, roles, groups, policies)**

```bash
aws iam get-account-authorization-details
```