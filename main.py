import requests
import urllib.request
import time
from bs4 import BeautifulSoup

from product import Product

base_url = 'https://www.ceneo.pl/'
product_key = '90654635'
# Get content of site containing product opinions
response = requests.get(base_url+product_key)

with open('index.html') as file:
    soup = BeautifulSoup(response.text, 'html.parser')
product = Product(soup)
print(product.average_score)
