import requests
import urllib.request
import time
import math
from bs4 import BeautifulSoup


class Product:
    base_url = 'https://www.ceneo.pl'
    opinions_per_page = 10

    def __init__(self):
        pass

    @staticmethod
    def scrap_page(link):
        return BeautifulSoup(requests.get(link).text, 'html.parser')

    @staticmethod
    def has_opinions(product_code):
        page = Product.scrap_page(Product.base_url+'/'+product_code)
        if page.find(class_='page-tab reviews'):
            return True
        else:
            return False

    @staticmethod
    def dict(product_code):
        pages = Product.scrap_opinion_pages(product_code)
        name_attr = 'product-top-2020__product-info__name'
        name = pages[0].find(class_=name_attr).text
        opinions = Product.get_all_opinions(pages)
        positives_count = sum(len(opinion['positives'])
                              for opinion in opinions)
        negatives_count = sum(len(opinion['negatives'])
                              for opinion in opinions)
        average_score = round(sum(opinion['score']
                                  for opinion in opinions)/len(opinions), 1)
        return {
            "code": product_code,
            "name": pages[0].find(class_=name_attr).text,
            "opinions": opinions,
            "opinions_count": len(opinions),
            "positives_count": positives_count,
            "negatives_count": negatives_count,
            "average_score": average_score,
            "score_stats": Product.get_score_stats(opinions),
            "recommendations": Product.get_recommendation_stats(opinions)
        }

    @staticmethod
    def scrap_opinion_pages(product_code):
        pages = []
        pages.append(Product.scrap_page(
            Product.base_url+'/'+product_code+'/opinie-1'))
        reviews_button = pages[0].find(class_='page-tab reviews active')
        if reviews_button:
            pages_count_str = reviews_button.find('span').text
            pages_count = math.ceil(int(pages_count_str[pages_count_str.find(
                '(')+1:pages_count_str.find(')')]) / Product.opinions_per_page)
        else:
            pages_count = 1
        for i in range(2, pages_count+1):
            page_link = f'{Product.base_url}/{product_code}/opinie-{i}'
            pages.append(Product.scrap_page(page_link))
        return pages

    @staticmethod
    def get_all_opinions(pages):
        opinions = []
        opinion_attr = 'user-post user-post__card js_product-review'
        for page in pages:
            for scrapped_opinion in page.find_all(class_=opinion_attr):
                opinions.append(Product.get_opinion(scrapped_opinion))
        return opinions

    def get_opinion(opinion):
        return {
            'id': opinion['data-entry-id'],
            'author': opinion.find(class_='user-post__author-name').text.strip("\n"),
            'recommendation': Product.get_recommendation(opinion),
            'score': float(opinion.find(class_='user-post__score-count').text[:-2].replace(',', '.')),
            'is_confirmed': 'Tak' if (opinion.find(class_='review-pz')) else 'Nie',
            'issue_date': Product.get_opinion_dates(opinion)['issue'],
            'purchase_date': Product.get_opinion_dates(opinion)['purchase'],
            'votes_yes': opinion.find(class_='vote-yes')['data-total-vote'],
            'votes_no': opinion.find(class_='vote-no')['data-total-vote'],
            'contents': opinion.find(class_='user-post__text').text,
            'positives': Product.get_opinion_features(opinion, 'positives'),
            'negatives': Product.get_opinion_features(opinion, 'negatives')
        }

    @staticmethod
    def get_recommendation(opinion):
        if opinion.find(class_='recommended'):
            return opinion.find(class_='recommended').text
        elif opinion.find(class_='not-recommended'):
            return opinion.find(class_='not-recommended').text
        else:
            return ''

    @staticmethod
    def get_opinion_dates(opinion):
        date_element = opinion.find(class_='user-post__published')('time')
        dates = [time['datetime']
                 [:time['datetime'].find(' ')] for time in date_element]
        dates_dict = {}
        dates_dict['issue'] = dates[0]
        if len(dates) > 1:
            dates_dict['purchase'] = dates[1]
        else:
            dates_dict['purchase'] = dates[0]
        return dates_dict

    @staticmethod
    def get_opinion_positives(opinion):
        if opinion.find(class_='review-feature__title--positives'):
            positives = [item.text for item in op.find(
                class_='review-feature__title--positives').parent(class_='review-feature__item')]
        else:
            positives = ''

    @staticmethod
    def get_opinion_features(opinion, type):
        feature_attr = 'review-feature__title--'+type
        parent_attr = 'review-feature__item'
        if opinion.find(class_=feature_attr):
            container = opinion.find(class_=feature_attr).parent(
                class_=parent_attr)
            features = [item.text for item in container]
            return features
        else:
            return ''
    
    @staticmethod
    def get_score_stats(opinions):
        score_stats = [0, 0, 0, 0, 0]
        for opinion in opinions:
            if opinion['score'] <= 1:
                score_stats[0] += 1
            elif opinion['score'] <= 2:
                score_stats[1] += 1
            elif opinion['score'] <= 3:
                score_stats[2] += 1
            elif opinion['score'] <= 4:
                score_stats[3] += 1
            else:
                score_stats[4] += 1

        return score_stats

    @staticmethod
    def get_recommendation_stats(opinions):
        recommendations = [0, 0, 0]
        for opinion in opinions:
            if opinion['recommendation'] == 'Polecam':
                recommendations[2] += 1
            elif opinion['recommendation'] == 'Nie polecam':
                recommendations[1] += 1
            else:
                recommendations[0] += 1
        return recommendations  