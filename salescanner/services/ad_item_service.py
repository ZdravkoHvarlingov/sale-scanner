from salescanner.model.ad_item import AdItem
class AdItemService:

    @staticmethod
    def process_new_ads(ads):
        print('Ad Item service called.')
        print(f'Number of ads: {len(ads)}')
        print(ads[0])
