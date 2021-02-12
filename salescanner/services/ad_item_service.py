import time
import pytz
import enchant
from datetime import datetime
from nltk.tokenize import RegexpTokenizer
from salescanner.repositories.ad_item_repository import AdItemRepository


class AdItemService:

    DEFAULT_ORDER_BY_ATTRIBUTE = 'score'
    DEFAULT_PAGE_SIZE = 20
    
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

    @staticmethod
    def list_ads(query_string, order_attribute=DEFAULT_ORDER_BY_ATTRIBUTE, page=0, size=DEFAULT_PAGE_SIZE):
        if order_attribute is None:
            order_attribute = AdItemService.DEFAULT_ORDER_BY_ATTRIBUTE
        if page is None:
            page = 0
        if size is None:
            size = AdItemService.DEFAULT_PAGE_SIZE

        ads_page = AdItemRepository.find_by_query(query_string, order_attribute, page, size)
        timezone = pytz.timezone('Europe/Sofia')
        for ad in ads_page.get('hits', []):
            upload_time = ad.get('source', {}).get('upload_time')
            if upload_time is not None:
                utc_dt = datetime.utcfromtimestamp(upload_time / 1000)
                utc_dt = utc_dt.replace(tzinfo=pytz.utc)
                upload_time = utc_dt.astimezone(timezone)
                
            ad['source']['upload_time'] = upload_time.isoformat()
        return ads_page

    @staticmethod
    def count_ads():
        return AdItemRepository.count_ads()
