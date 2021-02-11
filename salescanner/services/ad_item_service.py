from salescanner.repositories.ad_item_repository import AdItemRepository


class AdItemService:

    @staticmethod
    def process_new_ads(ads):
        for ad in ads:
            ad['literacy'] = AdItemService.calculate_literacy_score(ad)

        AdItemRepository.insert_list(ads)

    @staticmethod
    def calculate_literacy_score(ad):
        return 90
