import time
import enchant
from nltk.tokenize import RegexpTokenizer
from salescanner.repositories.ad_item_repository import AdItemRepository


class AdItemService:

    tokenizer = RegexpTokenizer(r'\w+')
    dictionary = enchant.Dict('bg_BG')

    @staticmethod
    def process_new_ads(ads):
        start = time.time()
        for ad in ads:
            ad['literacy'] = AdItemService.calculate_literacy_score(ad)
        end = time.time()
        print(f'Literacy calculation took {end - start}s')

        AdItemRepository.insert_list(ads)

    @staticmethod
    def calculate_literacy_score(ad):
        tokens = AdItemService.tokenizer.tokenize(ad.get('description', ''))
        tokens = set([token for token in tokens if len(token) > 2])
        if len(tokens) == 0:
            return 100

        correctly_written = 0
        for token in tokens:
            if AdItemService.dictionary.check(token):
                correctly_written += 1
        
        score = int(100 * correctly_written / len(tokens))
        return score
