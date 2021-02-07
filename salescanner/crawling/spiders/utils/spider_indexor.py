class SpiderIndexor:

    _spider_mapper = dict()

    def __init__(self, site_name):
        self._site_name = site_name
    
    def __call__(self, spider_class):
        SpiderIndexor._spider_mapper[self._site_name] = spider_class
        return spider_class

    @staticmethod
    def get_spider(site_name):
        return SpiderIndexor._spider_mapper.get(site_name)
    
    @staticmethod
    def get_spiders():
        return SpiderIndexor._spider_mapper.items()
