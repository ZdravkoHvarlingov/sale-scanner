from salescanner.crawling.spiders.utils.spider_indexor import SpiderIndexor
import scrapy
import logging

from datetime import datetime, timedelta
from salescanner.crawling.spiders.utils.utils import Utils
from salescanner.crawling.items import SalescannerItem


@SpiderIndexor('bazar')
class BazarAdsSpider(scrapy.Spider):

    MAX_NUMBER_OF_PAGES = 30
    name = 'bazar_sales'

    def __init__(self, **kwargs):
        self.allowed_domains = ['bazar.bg']
        self.start_urls = ['https://bazar.bg/obiavi?sort=date']
        self.pages_processed = 0

        super().__init__(**kwargs)
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        print(f'BAZAR LIST PAGE: {response.url}')
        offers_response = response.css('.search_cont_thumb .listItemContainer > .listItemLink::attr(href)')
        offers_urls = set(offers_response.getall())

        for offer_url in offers_urls:
            yield scrapy.Request(offer_url, callback=self.parse_details_page)
        self.pages_processed += 1

        next_page_url = response.css('.paging > .btn.next::attr(href)').get()
        if next_page_url is not None and self.pages_processed < BazarAdsSpider.MAX_NUMBER_OF_PAGES:
            yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)
        

    def parse_details_page(self, response):
        image_url = response.css('.mpic img.picture::attr(src)').get()
        title = response.css('h1.adName::text').get()
        price = response.css('.adPrice span.price::text').get()
        description = response.css('.bObiavaItem > div[itemprop="description"].text *::text').getall()
        description = ' '.join([line.strip() for line in description])
        upload_datetime = response.css('.adPlace > span.adDate::text').get()
        
        ad_item = SalescannerItem()
        ad_item['url'] = response.url
        ad_item['title'] = title.strip() if title else title
        ad_item['price'] = price.strip() if price else price
        ad_item['image_url'] = 'https:' + image_url if image_url and image_url.startswith('//') else image_url
        ad_item['description'] = description
        ad_item['upload_time'] = self.parse_upload_datetime(upload_datetime)
        yield ad_item

    def parse_upload_datetime(self, datetime_str):
        if datetime_str is None:
            return None

        datetime_str = datetime_str.strip()
        datetime_str = datetime_str.split(' ')
        if 'вчера' in datetime_str or 'днес' in datetime_str:
            return self.parse_recent_datetime(datetime_str)
        else:
            return self.parse_month_datetime(datetime_str)

    def parse_recent_datetime(self, datetime_split):
        # 'Публикувана/обновена вчера в 21:31 ч.'
        result_datetime = datetime.now()
        if 'вчера' in datetime_split:
            result_datetime -= timedelta(days=1)
        
        hour_minute = datetime_split[-2].split(':')
        return result_datetime.replace(
            hour=int(hour_minute[0]),
            minute=int(hour_minute[1]),
            second=0,
            microsecond=0)

    def parse_month_datetime(self, datetime_split):
        # 'Публикувана/обновена на 04 февруари в 13:18 ч.'
        # 'Публикувана/обновена на 08 декември 2020г. в 19:35 ч.'
              
        hour_minute = datetime_split[-2].split(':')
        day = int(datetime_split[2])

        year = datetime.now().year
        if len(datetime_split) == 8:
            year = int(datetime_split[4][0:-2])

        return datetime(
            year,
            Utils.month_to_number(datetime_split[3]),
            int(day),
            int(hour_minute[0]),
            int(hour_minute[1]))
