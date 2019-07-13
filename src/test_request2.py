import requests
r = requests.get('http://google.com')
print r.status_code
print r.headers
print r.text[0:1000]