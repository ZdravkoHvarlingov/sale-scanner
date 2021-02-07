from salescanner.salescanner.items import SalescannerItem
import scrapy
import logging
from datetime import datetime


class OLXAdsSpider(scrapy.Spider):

    MAX_NUMBER_OF_PAGES = 25
    name = 'olx_sales'

    def __init__(self, **kwargs):
        self.allowed_domains = ['olx.bg']
        self.start_urls = ['https://www.olx.bg/ads/']
        self.pages_processed = 0

        super().__init__(**kwargs)
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def parse(self, response):
        print(f'OLX LIST PAGE: {response.url}')
        offers_response = response.css('.offers')[1].css('.detailsLinkPromoted::attr(href), .detailsLink::attr(href)')
        offers_urls = set(offers_response.getall())

        for offer_url in offers_urls:
            yield scrapy.Request(offer_url, callback=self.parse_details_page)
        self.pages_processed += 1

        next_page_url = response.css('.next > a.pageNextPrev::attr(href)').get()
        if next_page_url is not None and self.pages_processed < OLXAdsSpider.MAX_NUMBER_OF_PAGES:
            yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)
        

    def parse_details_page(self, response):
        image_url = response.css('.descgallery__image img.bigImage::attr(src)').get()
        title = response.css('.offer-titlebox > h1::text').get()
        price = response.css('.offer-titlebox__price > .pricelabel > strong::text').get()
        description = response.css('.descriptioncontent > #textContent *::text').getall()
        description = ' '.join([line.strip() for line in description])
        upload_datetime = response.css('.offer-bottombar__items .offer-bottombar__item em strong::text').get()
        
        ad_item = SalescannerItem()
        ad_item['url'] = response.url
        ad_item['title'] = title.strip() if title else title
        ad_item['price'] = price.strip() if price else price
        ad_item['image_url'] = image_url
        ad_item['description'] = description
        ad_item['upload_time'] = self.parse_upload_datetime(upload_datetime)
        yield ad_item

    def parse_upload_datetime(self, datetime_str):
        if datetime_str is None:
            return None

        datetime_str = datetime_str.strip()
        datetime_str = datetime_str[2:].split(',')
        time_portion = datetime_str[0].split(':')
        date_portion = datetime_str[1].strip().split(' ')

        return datetime(
            int(date_portion[2]),
            self.month_to_number(date_portion[1]),
            int(date_portion[0]),
            int(time_portion[0]),
            int(time_portion[1]))

    def month_to_number(self, month_str):
        month_dict = {
            'януари': 1,
            'февруари': 2,
            'март': 3,
            'април': 4,
            'май': 5,
            'юни': 6,
            'юли': 7,
            'август': 8,
            'септември': 9,
            'октомври': 10,
            'ноември': 11,
            'декември': 12
        }

        return month_dict.get(month_str)
