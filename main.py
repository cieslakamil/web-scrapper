import requests
import urllib.request
import time
from bs4 import BeautifulSoup

from opinion import Opinion


base_url = 'https://www.ceneo.pl/'
product_key = '85615932'
# Get content of site containing product opinions
response = requests.get(base_url+product_key)

with open('index.html') as file:
    soup = BeautifulSoup(response.text, 'html.parser')

opinions_div = soup.find(
    class_='js_product-reviews js_reviews-hook js_product-reviews-container')
opinions = [Opinion(data) for data in opinions_div.find_all(
    class_='user-post user-post__card js_product-review', recursive=False)]

for opinion in opinions:
    print(opinion.id)
    print(opinion.author)
    print(opinion.recommendation)
    print(opinion.score)
    print(opinion.is_confirmed)
    print(opinion.date)
    print(f'{opinion.votes_yes}/{opinion.votes_no}')
    print(opinion.contents)
    print(opinion.positives)
    print(opinion.negatives)
    print('------------')
