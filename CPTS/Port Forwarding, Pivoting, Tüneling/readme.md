# Port Forwarding, Pivoting, Tunneling
**Lateral Movement (Yanal Hareket):** Aynı ağ segmenti içinde ele geçirilen bir hesabı kullanarak diğer makinelere yayılmaktır. *Örnek:* Bir Windows makinesinde yerel yönetici parolasının hash'ini bulup aynı parolayı kullanan diğer Windows sunucularına giriş yapmak.

**Pivoting:** Ele geçirdiğin bir host'u köprü olarak kullanıp doğrudan erişemediğin bir ağa geçmektir. *Örnek:* Hem `10.129.x.x` hem `172.16.5.0/23` ağına bağlı Ubuntu pivot host'unu kullanarak, Attack Host'tan `172.16.5.19` Windows sunucusuna ulaşmak.

**Tunneling (Tünelleme):** Trafiği başka bir protokolün içine gömerek taşımaktır. Güvenlik duvarları genelde izin verilen protokolü geçirir. *Örnek:* C2 trafiğini HTTP GET/POST istekleri gibi göstererek kurumsal ağdaki denetimleri atlatmak.

**Kısaca fark:** Lateral movement aynı ağda yayılmak, pivoting farklı bir ağa geçmek için cihazı köprü yapmak, tunneling ise bu bağlantının trafiğini kapsüllemek. Pivoting çoğu zaman tunneling kullanır ama tünel olmadan da pivot yapılabilir; port forwarding ve proxychains bunun basit örnekleridir.

----

# Port Forwarding

## SSH Local Port Forwarding

![ssh-port-porwarding](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/11.png)

#### Scanning the Pivot Target



```bash
nmap -sT -p22,3306 10.129.202.64


PORT     STATE  SERVICE
22/tcp   open   ssh
3306/tcp closed mysql
```

#### Target Makinadan Kendi Makinamıza Port Gönderme (Localde Port Forwarding)

<h2 style='color:red'>Bu işlemi yapabilmek için öncelikle target'da shell açmış  olmamız gerekiyor<h2>

```bash
ssh -L 1234:localhost:3306 ubuntu@10.129.202.64

# ssh -L my-ip'de-çalışıcak-port:o-makinadan-kendi-makinama-yönlendirme-yapıyroum-ama-buraya-yinede-localhost-yazıcaz:o-makinadaki-3306-portunu-gönderiyorum shell-aldığım-target-makina-username@shell-aldığım-targetmakina-ip-adresi
```

##### Başarılımı değilmi kontrol etme
**netstat**

```bash
netstat -antp | grep 1234



tcp        0      0 127.0.0.1:1234          0.0.0.0:*               LISTEN      4034/ssh            
tcp6       0      0 ::1:1234                :::*                    LISTEN      4034/ssh
```

**nmap**

```bash
nmap -v -sV -p1234 localhost

PORT     STATE SERVICE VERSION
1234/tcp open  mysql   MySQL 8.0.28-0ubuntu0.20.04.3

```

####  Target Makinadan Kendi Makinamıza Multiple Port Gönderme (Localde Port Forwarding)




```bash
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64

# 1234 ve 8080 benim makinamda çalışcıak port  
```


# Pivoting

![ssh-port-porwarding](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/158/22.png)

<h2 style='color:red'>Bu işlemi yapabilmek için öncelikle target'da shell açmış  olmamız gerekiyor<h2>

 Ubuntu (`target-makina`) ana bilgisayarında `ifconfig` komutunu yazarsanız,
 bu sunucunun birden fazla ağ arabirim kartına (NIC) sahip olduğunu göreceksiniz:

<ul style='font-size:1.3rem'>
<li>Saldırı ana bilgisayarımıza <u>bize</u> (<code>ens192</code>) bağlı olan</li>
<li>Farklı bir ağ (<code>ens224</code>) içindeki diğer ana bilgisayarlarla iletişim kuran bir birim</li>
<li>
Geri döngü arayüzü <code>lo</code>.
    <ul>
      <li>Makinenin kendi kendisiyle konuşmasını sağlayan sanal ağ arayüzüdür (yani localhost veya 127.0.0.1 adresidir).</li>
    </ul>
</li>
</ul>



```bash
# TARGET MAKİNA

ubuntu@WEB01:~$ ifconfig 

ens192: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.129.202.64  netmask 255.255.0.0  broadcast 10.129.255.255
        inet6 dead:beef::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x0<global>
        inet6 fe80::250:56ff:feb9:52eb  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:52:eb  txqueuelen 1000  (Ethernet)
        RX packets 35571  bytes 177919049 (177.9 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10452  bytes 1474767 (1.4 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ens224: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.16.5.129  netmask 255.255.254.0  broadcast 172.16.5.255
        inet6 fe80::250:56ff:feb9:a9aa  prefixlen 64  scopeid 0x20<link>
        ether 00:50:56:b9:a9:aa  txqueuelen 1000  (Ethernet)
        RX packets 8251  bytes 1125190 (1.1 MB)
        RX errors 0  dropped 40  overruns 0  frame 0
        TX packets 1538  bytes 123584 (123.5 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 270  bytes 22432 (22.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 270  bytes 22432 (22.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Hangi porta erişmemiz gerektiğini bildiğimiz önceki senaryonun aksine, <u>mevcut senaryomuzda ağın diğer tarafında hangi hizmetlerin bulunduğunu bilmiyoruz</u>

Bu nedenle, ağ üzerindeki daha küçük IP aralıklarını (`172.16.5.1-200`) veya tüm alt ağı (`172.16.5.0/23`) tarayabiliriz. Bu taramayı doğrudan saldırı makinemizden gerçekleştiremeyiz;


çünkü makinemizin `172.16.5.0/23` ağına giden herhangi bir rotası bulunmamaktadır. Bunu yapabilmek için dinamik port yönlendirme (`dynamic port forwarding`) yöntemini kullanmalı ve ağ paketlerimizi Ubuntu sunucusu üzerinden yönlendirmeliyiz (`pivot` etmeliyiz).


Bunu gerçekleştirmek adına, yerel makinemizde (kişisel saldırı makinemiz) bir SOCKS dinleyicisi (listener) başlatırız.
Ardından hedef sunucuya bağlandıktan sonra, trafiği `SSH` tüneli üzerinden söz konusu ağa (`172.16.5.0/23`) yönlendirecek şekilde `SSH` yapılandırmasını ayarlayabiliriz.
