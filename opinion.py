class Opinion:
    def __init__(self, data):
        self.id = data['data-entry-id']
        self.author = data.find(class_='user-post__author-name').text.strip("\n")
        self.recommendation = data.find(class_='recommended').text
        self.score = data.find(class_='user-post__score-count').text
        self.is_confirmed = True if data .find(class_='review-pz') else False
        self.date = [time['datetime'] for time in data.find(class_='user-post__published').find_all('time')]
        self.votes_yes = data.find(class_='vote-yes')['data-total-vote']
        self.votes_no = data.find(class_='vote-no')['data-total-vote']
        self.contents = data.find(class_='user-post__text').text
        self.positives = []
        self.negatives = []
        for col in data.find_all(class_='review-feature__col'):
            features = [item.text for item in col.find_all(class_='review-feature__item')]
            if  col.find(class_='review-feature__title--positives'):
                self.positives = features
            elif  col.find(class_='review-feature__title--negatives'):
                self.negatives = features