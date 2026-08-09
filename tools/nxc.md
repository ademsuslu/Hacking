# nxc
[www.netexec.wiki/smb-protocol/scan-for-vulnerabilities](https://www.netexec.wiki/smb-protocol/scan-for-vulnerabilities)


```bash
nxc smb 10.10.10.161 -u '' -p ''
nxc smb 10.10.10.161 -u '' -p '' --shares
nxc smb 10.10.10.161 -u '' -p '' --pass-pol
nxc smb 10.10.10.161 -u '' -p '' --users
nxc smb 10.10.10.161 -u '' -p '' --groups
```
You can also reproduce this behavior with `smbclient` or `rpcclient`


```bash
rpcclient -N -U "" -L \\10.10.10.161
rpcclient $> enumdomusers
user:[bonclay] rid:[0x46e]
user:[zoro] rid:[0x46f]
```
