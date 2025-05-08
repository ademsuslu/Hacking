https://docs.aws.amazon.com/cli/latest/userguide/cli-services-s3-commands.html#using-s3-commands-listing-buckets

ilk olarak configrasyon
![image](https://github.com/user-attachments/assets/496b91aa-3d62-4811-996d-c0ff41e392fb)

```bash
aws s3 ls --endpoint-url http://s3.thetoppers.htb s3://thetoppers.htb
```

bu kısımdaki ls cmd oluyor

aws ile file upload
```bash
aws s3 cp <file> s3://thetoppers.htb --endpoint-url http://s3.thetoppers.htb
```

