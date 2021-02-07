import os
import json
from salescanner.salescanner.spiders.bazar_ads_spider import BazarAdsSpider
from salescanner.salescanner.spiders.olx_ads_spider import OLXAdsSpider
from scrapy.crawler import CrawlerProcess


if __name__ == "__main__":
  # os.remove('olx_ads.json')
  # process = CrawlerProcess({
  #   'FEED_FORMAT': 'json',
  #   'FEED_URI': 'olx_ads.json'
  # })
  # process.crawl(OLXAdsSpider)
  # process.start()

  # with open('olx_ads.json') as olx_ads_file:
  #   olx_ads = json.load(olx_ads_file)
  
  # print('END BRO')
  # print(f'ADS: {len(olx_ads)}')
  # print(olx_ads[0])

  if os.path.isfile('bazar_ads.json'):
    os.remove('bazar_ads.json')
  process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'bazar_ads.json'
  })
  process.crawl(BazarAdsSpider)
  process.start()

  with open('bazar_ads.json') as bazar_ads_file:
    bazar_ads = json.load(bazar_ads_file)
  
  print('END BRO')
  print(f'ADS: {len(bazar_ads)}')
  print(bazar_ads[0])
