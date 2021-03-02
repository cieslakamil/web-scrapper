import requests
import urllib.request
import time
import math
from bs4 import BeautifulSoup


class Product:
    def __init__(self, product_code):
        base_url = 'https://www.ceneo.pl/'
        self.first_page = BeautifulSoup(requests.get(
            base_url+product_code+'/opinie-1').text, 'html.parser')
        reviews_button = self.first_page.find(class_='page-tab reviews active')
        self.opinions_per_page = 10
        if reviews_button:
            raw_count = reviews_button.find('span').text
            self.pages_count = math.ceil(int(raw_count[raw_count.find('(')+1:raw_count.find(')')]) / self.opinions_per_page)
            print(self.pages_count)

        self.opinions = [self.get_opinion_data(raw_opinion) for raw_opinion in self.first_page.find_all(
            class_='user-post user-post__card js_product-review')]

    def get_opinion_data(self, op):
        opinion = {
            'id': op['data-entry-id'],
            'author': op.find(class_='user-post__author-name').text.strip("\n"),
            'recommended': bool(op.find(class_='recommended')),
            'score': op.find(class_='user-post__score-count').text,
            'is_confirmed': True if op .find(class_='review-pz') else False,
            'date': [time['datetime'] for time in op.find(class_='user-post__published')('time')],
            'votes_yes': op.find(class_='vote-yes')['data-total-vote'],
            'votes_no': op.find(class_='vote-no')['data-total-vote'],
            'contents': op.find(class_='user-post__text').text,
            # Below are three ways in which positives and negatives can be extracted:
            # option 1
            # 'positives': [item.text for item in op.find(class_='review-feature__title--positives').parent(class_='review-feature__item')] if op.find(class_='review-feature__title--positives') else [],
            # 'negatives': [item.text for item in op.find_all(class_='review-feature__item') if item.parent.find(class_='review-feature__title--negatives')]
        }
        # option 2
        for col in op(class_='review-feature__col'):
            features = [item.text for item in col.find_all(
                class_='review-feature__item')]
            if col.find(class_='review-feature__title--positives'):
                opinion['positives'] = features
            elif col.find(class_='review-feature__title--negatives'):
                opinion['negatives'] = features
        # option 3
        '''
        if op.find(class_='review-feature__title--positives'):
            opinion['positives'] = [item.text for item in op.find(
                class_='review-feature__title--positives').parent(class_='review-feature__item')]
        if op.find(class_='review-feature__title--negatives'):
            opinion['negatives'] = [item.text for item in op.find(
                class_='review-feature__title--negatives').parent(class_='review-feature__item')]
        '''
        return opinion
