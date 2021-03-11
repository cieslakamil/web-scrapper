import requests
import urllib.request
import time
import math
from bs4 import BeautifulSoup


class Product:
    def __init__(self, code):
        self.code = code
        self.base_url = 'https://www.ceneo.pl/'
        pages = self.scrap_pages()
        self.name = pages[0].find(
            class_='product-top-2020__product-info__name').text
        self.opinions = self.get_all_opinions(pages)
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

    def scrap_pages(self):
        opinions_per_page = 10
        pages = []
        pages.append(self.scrap_page(self.base_url+self.code+'/opinie-1'))
        reviews_button = pages[0].find(class_='page-tab reviews active')
        if reviews_button:
            pages_count_str = reviews_button.find('span').text
            pages_count = math.ceil(int(pages_count_str[pages_count_str.find(
                '(')+1:pages_count_str.find(')')]) / opinions_per_page)
        else:
            pages_count = 1
        for i in range(2, pages_count+1):
            pages.append(self.scrap_page(
                self.base_url+self.code+'/opinie-'+str(i)))
        return pages

    def scrap_page(self, link):
        return BeautifulSoup(requests.get(link).text, 'html.parser')

    def get_all_opinions(self, pages):
        opinions = []
        #opinions = [self.get_opinion_data(d) for d in page.find_all(class_='user-post user-post__card js_product-review') for page in pages]
        for page in pages:
            for raw_opinion in page.find_all(class_='user-post user-post__card js_product-review'):
                opinions.append(self.get_opinion(raw_opinion))
        return opinions

    def get_opinion(self, op):
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
