import os
import json
import time
import multiprocessing

from scrapy.crawler import CrawlerProcess
from salescanner.crawling.spiders import SpiderIndexor


class SiteCrawler:

    @staticmethod
    def crawl():
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
            with open(f'{site}_ads.json') as ads_file:
                site_ads = json.load(ads_file)
            ads.extend(site_ads)
        end = time.time()

        print(f'Crawling ended in {end - start} seconds')
        print(f'Number of ads: {len(ads)}')
        print(ads[0])
    
    @staticmethod
    def _crawl_site(site, spider):
        json_file = f'{site}_ads.json'
        if os.path.isfile(json_file):
            os.remove(json_file)

        process = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': json_file
        })
        process.crawl(spider)
        process.start()
