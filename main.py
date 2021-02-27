import requests
import urllib.request
import time
from bs4 import BeautifulSoup

url = 'https://www.ceneo.pl/90654635'
response = requests.get(url)

with open('index.html') as file:
    soup = BeautifulSoup(response.text, 'html.parser')

print(soup.title)
