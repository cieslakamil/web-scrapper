class Product:
    def __init__(self, scrapped_data):
        self.scrapped_data = scrapped_data
        self.opinions = [self.get_opinion(raw_opinion) for raw_opinion in self.scrapped_data.find_all(
            class_='user-post user-post__card js_product-review')]
        self.opinions_count = len(self.opinions)
        self.positives_count = sum(len(opinion['positives']) for opinion in self.opinions)
        self.negatives_count = sum(len(opinion['negatives']) for opinion in self.opinions)
        self.average_score = sum(opinion['score'] for opinion in self.opinions)/self.opinions_count
    def get_opinion(self, raw_opinion):
        opinion = {
            'id': raw_opinion['data-entry-id'],
            'author': raw_opinion.find(class_='user-post__author-name').text.strip("\n"),
            'recommendation': raw_opinion.find(class_='recommended').text,
            'score': float(raw_opinion.find(class_='user-post__score-count').text[:-2].replace(',','.')),
            'is_confirmed': True if raw_opinion .find(class_='review-pz') else False,
            'date': [time['datetime'] for time in raw_opinion.find(class_='user-post__published')('time')],
            'votes_yes': raw_opinion.find(class_='vote-yes')['data-total-vote'],
            'votes_no': raw_opinion.find(class_='vote-no')['data-total-vote'],
            'contents': raw_opinion.find(class_='user-post__text').text,
            'positives': [],
            'negatives': []
            # Below are three ways in which positives and negatives can be extracted:
            # option 1
            #'positives': [item.text for item in raw_opinion.find(class_='review-feature__title--positives').parent(class_='review-feature__item')] if raw_opinion.find(class_='review-feature__title--positives') else [],
            #'negatives': [item.text for item in raw_opinion.find_all(class_='review-feature__item') if item.parent.find(class_='review-feature__title--negatives')]
        }
        # option 2
        for col in raw_opinion(class_='review-feature__col'):
            features = [item.text for item in col.find_all(
                class_='review-feature__item')]
            if col.find(class_='review-feature__title--positives'):
                opinion['positives'] = features
            elif col.find(class_='review-feature__title--negatives'):
                opinion['negatives'] = features
        # option 3
        '''
        if raw_opinion.find(class_='review-feature__title--positives'):
            opinion['positives'] = [item.text for item in raw_opinion.find(
                class_='review-feature__title--positives').parent(class_='review-feature__item')]
        if raw_opinion.find(class_='review-feature__title--negatives'):
            opinion['negatives'] = [item.text for item in raw_opinion.find(
                class_='review-feature__title--negatives').parent(class_='review-feature__item')]
        '''
        return opinion
