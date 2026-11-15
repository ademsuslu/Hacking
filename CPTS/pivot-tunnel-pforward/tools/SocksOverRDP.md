



### Regsvr32.exe kullanarak SocksOverRDP.dll Yükleme

+ `https://github.com/nccgroup/SocksOverRDP/releases`
+ `https://www.proxifier.com/download/#win-tab`


```cmd
C:\Users\htb-student\Desktop\SocksOverRDP-x64> regsvr32.exe SocksOverRDP-Plugin.dll
```

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/socksoverrdpdll.png)

Şimdi `mstsc.exe` kullanarak `172.16.5.19` adresine RDP ile bağlanabiliriz. Bağlanırken SocksOverRDP eklentisinin etkin olduğuna ve `127.0.0.1:1080` portunu dinlediğine dair bir uyarı almalıyız. Bağlanmak için `victor:pass@123` kimlik bilgilerini kullanabiliriz.

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/pivotingtoDC.png)

`SocksOverRDP-x64.zip` veya sadece `SocksOverRDP-Server.exe` dosyasını `172.16.5.19` (C Makinesi) hedefine aktarmamız gerekecek. Daha sonra `SocksOverRDP-Server.exe`'yi Yönetici (Admin) ayrıcalıklarıyla başlatabiliriz.

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/executingsocksoverrdpserver.png)

İlk ele geçirdiğimiz makineye (B Makinesi) geri dönüp Netstat ile kontrol ettiğimizde, SOCKS dinleyicimizin `127.0.0.1:1080` üzerinde başladığını görmeliyiz.

### SOCKS Dinleyicisinin Başladığını Doğrulama

```cmd
netstat -ant | findstr 1080

 TCP    127.0.0.1:1080         0.0.0.0:0              LISTENING
```

Dinleyicimizi başlattıktan sonra, Proxifier taşınabilir sürümünü Windows 10 hedefine (B makinesi) aktarabilir ve tüm paketlerimizi `127.0.0.1:1080` adresine iletecek şekilde yapılandırabiliriz. Proxifier, trafiği belirtilen sunucu ve port üzerinden yönlendirecektir. Proxifier'ı yapılandırmanın hızlı bir özeti için aşağıdaki klibi (gif) inceleyin.

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/configuringproxifier.gif)

Proxifier yapılandırılıp çalıştırıldığında `mstsc.exe`'yi başlatabiliriz. Proxifier tüm trafiğimizi `127.0.0.1:1080`'e yönlendirecek, bu da trafiği RDP üzerinden `172.16.5.19`'a tünelledikten sonra `SocksOverRDP-Server.exe` kullanılarak `172.16.5.155` adresine iletecektir.

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/rdpsockspivot.png)

### RDP Performans Hususları

Bir sızma testi (engagement) sırasında RDP oturumlarımızla etkileşime girerken, özellikle aynı anda birden fazla RDP oturumu yönetiyorsak, yavaş performansla karşılaşabiliriz. Eğer durum buysa, `mstsc.exe` içindeki **Experience (Deneyim)** sekmesine gidip **Performance (Performans)** ayarını **Modem** olarak değiştirebiliriz.

![win](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/rdpexpen.png)