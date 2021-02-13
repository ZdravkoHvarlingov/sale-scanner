import os
import json
import time
import multiprocessing

from scrapy.crawler import CrawlerProcess
from salescanner.crawling.spiders import SpiderIndexor
from salescanner.services.ad_item_service import AdItemService


class SiteCrawler:

    INTERVAL_IN_SECONDS = 300

    @staticmethod
    def crawl():
        while True:
            try:
                print('Starting crawling operation...')
                SiteCrawler._perform_crawling()
                time.sleep(SiteCrawler.INTERVAL_IN_SECONDS)
            except:
                print('Exception ocurred during crawl operation. Retrying bulk in 3 seconds because of OS slow file operations.')
                time.sleep(3)
                SiteCrawler._retry_bulk()
        
    @staticmethod
    def _perform_crawling():
        start = time.time()
        processes = []
        for site, spider in SpiderIndexor.get_spiders():
            site_process = multiprocessing.Process(target=SiteCrawler._crawl_site, args=(site, spider))
            site_process.daemon = True
            site_process.start()
            processes.append((site, site_process))

        ads = []
        for site, process in processes:
            process.join()
            with open(f'ads_json/{site}_ads.json') as ads_file:
                site_ads = json.load(ads_file)
            ads.extend(site_ads)
        end = time.time()

        print(f'Crawling ended in {end - start} seconds')
        AdItemService.process_new_ads(ads)

    @staticmethod
    def _retry_bulk():
        try:
            ads = []
            for site, _ in SpiderIndexor.get_spiders():
                with open(f'ads_json/{site}_ads.json') as ads_file:
                    site_ads = json.load(ads_file)
                ads.extend(site_ads)
            
            AdItemService.process_new_ads(ads)
        except:
            print('Could not load json files of the crawled ads. Bulk retry failed')

    @staticmethod
    def _crawl_site(site, spider):
        json_file = f'ads_json/{site}_ads.json'
        if os.path.isfile(json_file):
            os.remove(json_file)

        process = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': json_file
        })
        process.crawl(spider)
        process.start()


if __name__ == "__main__":
    SiteCrawler.crawl()
