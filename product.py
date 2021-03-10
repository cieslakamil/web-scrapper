import requests
import urllib.request
import time
import math
from bs4 import BeautifulSoup


class Product:
    def __init__(self, product_code):
        self.code = product_code
        base_url = 'https://www.ceneo.pl/'
        first_page = self.scrap_page(base_url+product_code+'/opinie-1')
        reviews_button = first_page.find(class_='page-tab reviews active')
        self.name = first_page.find(
            class_='product-top-2020__product-info__name').text
        opinions_per_page = 10
        if reviews_button:
            raw_count = reviews_button.find('span').text
            pages_count = math.ceil(int(raw_count[raw_count.find(
                '(')+1:raw_count.find(')')]) / opinions_per_page)
        else:
            pages_count = 0

        pages = []
        for i in range(1, pages_count+1):
            pages.append(self.scrap_page(
                base_url+product_code+'/opinie-'+str(i)))

        self.opinions = []
        for page in pages:
            for raw_opinion in page.find_all(class_='user-post user-post__card js_product-review'):
                self.opinions.append(self.get_opinion_data(raw_opinion))
        self.opinions_count = len(self.opinions)
        self.positives_count = sum(
            len(opinion['positives']) for opinion in self.opinions)
        self.negatives_count = sum(
            len(opinion['negatives']) for opinion in self.opinions)
        self.average_score = round(sum(
            opinion['score'] for opinion in self.opinions)/self.opinions_count, 1)


        self.score_stats = [0, 0, 0, 0, 0]
        for opinion in self.opinions:
            if opinion['score'] <= 1:
                self.score_stats[0] += 1
            elif opinion['score'] <= 2:
                self.score_stats[1] += 1
            elif opinion['score'] <= 3:
                self.score_stats[2] += 1
            elif opinion['score'] <= 4:
                self.score_stats[3] += 1
            else:
                self.score_stats[4] += 1

        # none/negative/positive
        self.recommendations = [0, 0, 0]
        for opinion in self.opinions:
            if opinion['recommendation'] == 'Polecam':
                self.recommendations[2] += 1
            elif opinion['recommendation'] == 'Nie Polecam':
                self.recommendations[1] += 1
            else:
                self.recommendations[0] += 1


    def get_properties(self):
        return {
            "code": self.code,
            "name": self.name,
            "opinions": self.opinions,
            "opinions_count": self.opinions_count,
            "positives_count": self.positives_count,
            "negatives_count": self.negatives_count,
            "average_score": self.average_score,
            "score_stats": self.score_stats,
            "recommendations": self.recommendations
        }

    def scrap_page(self, link):
        return BeautifulSoup(requests.get(link).text, 'html.parser')

    def get_opinion_data(self, op):
        if op.find(class_='recommended'):
            recommendation = op.find(class_='recommended').text
        elif op.find(class_='not-recommended'):
            recommendation = op.find(class_='not-recommended').text
        else:
            recommendation = ''

        dates = [time['datetime'][:time['datetime'].find(' ')]
                 for time in op.find(class_='user-post__published')('time')]

        if op.find(class_='review-feature__title--positives'):
            positives = [item.text for item in op.find(
                class_='review-feature__title--positives').parent(class_='review-feature__item')]
        else:
            positives = ''
        if op.find(class_='review-feature__title--negatives'):
            negatives = [item.text for item in op.find(
                class_='review-feature__title--negatives').parent(class_='review-feature__item')]
        else:
            negatives = ''

        opinion = {
            'id': op['data-entry-id'],
            'author': op.find(class_='user-post__author-name').text.strip("\n"),
            'recommendation': recommendation,
            'score': float(op.find(class_='user-post__score-count').text[:-2].replace(',', '.')),
            'is_confirmed': 'Tak' if (op.find(class_='review-pz')) else 'Nie',
            'issue_date': dates[0],
            # check whether the dat of purchase is different than the date of issuing an opinion
            'purchase_date': dates[1] if len(dates) > 1 else dates[0],
            'votes_yes': op.find(class_='vote-yes')['data-total-vote'],
            'votes_no': op.find(class_='vote-no')['data-total-vote'],
            'contents': op.find(class_='user-post__text').text,
            'positives': positives,
            'negatives': negatives
        }
        return opinion
