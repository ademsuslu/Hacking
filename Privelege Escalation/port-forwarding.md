# kendi terminalimden port forwarding

```bash
sshpass -p 'target_password' ssh target_username@target_ip -L 8765:127.0.0.1:8765 

sshpass -p 'X1l9fx1ZjS7RZb' ssh john@1.2.3.4 -L 8765:127.0.0.1:8765 
```
# veya

```bash
ssh -L my-ip:8080:target-ip:80 target-user@target-ip
```
