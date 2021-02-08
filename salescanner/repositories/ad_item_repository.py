from elasticsearch import Elasticsearch
from elasticsearch import helpers


class AdItemRepository:

    INDEX_MAPPING = {
        'mappings': {
			'properties': {
				'description': {
					'type': 'text',
					'fields': {
						'keyword': {
							'type': 'keyword',
							'ignore_above': 256
						}
					}
				},
				'image_url': {
					'type': 'text',
					'fields': {
						'keyword': {
							'type': 'keyword',
							'ignore_above': 256
						}
					}
				},
				'price': {
					'type': 'text',
					'fields': {
						'keyword': {
							'type': 'keyword',
							'ignore_above': 256
						}
					}
				},
				'title': {
					'type': 'text',
					'fields': {
						'keyword': {
							'type': 'keyword',
							'ignore_above': 256
						}
					}
				},
				'upload_time': {
					'type': 'long'
				},
				'url': {
					'type': 'text',
					'fields': {
						'keyword': {
							'type': 'keyword',
							'ignore_above': 256
						}
					}
				}
			}
		}
    }

    def __init__(self):
        self._es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
        if not self._es.ping():
            raise ValueError("Connection failed")
        
        if not self._es.indices.exists('ads'):
            self._es.indices.create('ads', body=AdItemRepository.INDEX_MAPPING)
        print(self._es.indices.exists('ads'))
        
        # self.insert_one()
        self.bulk()

        self._es.indices.refresh('ads')
        print(self._es.cat.count('ads', params={"format": "json"}))
        print(self._es.indices.get('ads'))

    def bulk(self):
        docs = [
            {"url": "https://www.olx.bg/ad/renault-scenic-na-chasti-CID360-ID7zPVy.html", "title": "Renault Scenic \u043d\u0430 \u0447\u0430\u0441\u0442\u0438", "price": "250 \u043b\u0432.", "image_url": "https://frankfurt.apollo.olxcdn.com:443/v1/files/ilajnn8c0pot-BG/image;s=800x600", "description": "\u0410\u0432\u0442\u043e\u043c\u043e\u0440\u0433\u0430 \u201c\u0421\u043e\u043a\u043e\u043b \u041e\u041e\u0414\u201d \u0441\u0435 \u043d\u0430\u043c\u0438\u0440\u0430 \u0432 \u0441. \u0421\u043e\u043a\u043e\u043b \u043e\u0431\u0449\u0438\u043d\u0430 \u041d\u043e\u0432\u0430 \u0417\u0430\u0433\u043e\u0440\u0430. \u0424\u0438\u0440\u043c\u0430\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0432\u0430 \u0432\u0442\u043e\u0440\u0430 \u0443\u043f\u043e\u0442\u0440\u0435\u0431\u0430 \u0430\u0432\u0442\u043e \u0447\u0430\u0441\u0442\u0438 \u0437\u0430   \u0432\u0441\u0438\u0447\u043a\u0438 \u043c\u043e\u0434\u0435\u043b\u0438 \u043a\u043e\u043b\u0438. \u0420\u0430\u0431\u043e\u0442\u0438\u043c \u0441 \u0432\u0441\u0438\u0447\u043a\u0438 \u043a\u0443\u0440\u0438\u0435\u0440\u0441\u043a\u0438 \u0444\u0438\u0440\u043c\u0438 \u043f\u043e \u0438\u0437\u0431\u043e\u0440 \u043d\u0430 \u043a\u043b\u0438\u0435\u043d\u0442\u0430. \u0420\u0430\u0437\u043f\u043e\u043b\u0430\u0433\u0430\u043c\u0435 \u0441 \u0447\u0430\u0441\u0442\u0438 \u0432\u0442\u043e\u0440\u0430 \u0443\u043f\u043e\u0442\u0440\u0435\u0431\u0430 \u0437\u0430 \u0442\u043e\u0437\u0438 \u0438 \u043e\u0449\u0435 \u0434\u0440\u0443\u0433\u0438 \u043c\u043e\u0434\u0435\u043b\u0438 \u0430\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u0438. \u0422\u0435\u043b\u0435\u0444\u043e\u043d \u0437\u0430 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 : 883 - \u041f\u043e\u043a\u0430\u0436\u0438 - ", "upload_time": 1231212312},
            {"url": "https://www.olx.bg/ad/nike-airmax-270-39nomer-CID655-ID8krRz.html", "title": "Nike airmax 270 39\u043d\u043e\u043c\u0435\u0440", "price": "200 \u043b\u0432.", "image_url": "https://frankfurt.apollo.olxcdn.com:443/v1/files/s7ucbygdk10c3-BG/image;s=800x600", "description": "\u041c\u0430\u0440\u0430\u0442\u043e\u043d\u043a\u0438\u0442\u0435 \u0441\u0430 \u0447\u0438\u0441\u0442\u043e \u043d\u043e\u0432\u0438 \u043e\u0440\u0438\u0433\u0438\u043d\u0430\u043b\u043d\u0438 Unisex \u0437\u0430 \u043c\u044a\u0436\u0435 \u0438 \u0436\u0435\u043d\u0438.", "upload_time": 123131231},
            {"url": "https://www.olx.bg/ad/245-45-18-hankok-CID360-ID8eBQx.html", "title": "245/45/18 \u0425\u0430\u043d\u043a\u043e\u043a", "price": "120 \u043b\u0432.", "image_url": "https://frankfurt.apollo.olxcdn.com:443/v1/files/znv6trxpfkwf-BG/image;s=800x600", "description": "\u041b\u0435\u0442\u043d\u0438 \u0413\u0443\u043c\u0438 2 \u0431\u0440\u043e\u044f \u0425\u0430\u043d\u043a\u043e\u043a . \u0415\u0434\u043d\u0442\u0430\u0442\u0430 \u0438\u043c\u0430 \u041b\u0435\u043f\u0435\u043d\u043a\u0430  , \u041d\u0430 \u0414\u0440\u0443\u0433\u0430\u0442\u0430 \u041b\u0438\u043f\u0441\u0432\u0430 \u041c\u0430\u043b\u043a\u043e \u0413\u0440\u0430\u0439\u0444\u0435\u0440 - \u0421\u043d\u0438\u043c\u0430\u043b \u0441\u044a\u043c \u0413\u043e - \u0414\u041e\u0422 1 \u0431\u0440\u043e\u0439 - 2016\u0433 - 7.22\u043c\u043c. 1\u0431\u0440\u043e\u0439 - 2015\u0433 - 7.68\u043c\u043c. \u0426\u0435\u043d\u0430 \u0437\u0430 \u0414\u0432\u0435\u0442\u0435 \u0413\u0443\u043c\u0438 - 120\u043b\u0432", "upload_time": 918723912}
        ]

        actions = [
            {
                "_index": "ads",
                "_id": ad['url'],
                "_source": ad
            }
            for ad in docs
        ]
        helpers.bulk(self._es, actions)

    
    def insert_one(self):
        doc = {"url": "https://www.olx.bg/ad/ted-baker-nova-roklya-razmer-1-CID655-ID85NpA.html", "title": "2Ted Baker \u043d\u043e\u0432\u0430 \u0440\u043e\u043a\u043b\u044f, \u0440\u0430\u0437\u043c\u0435\u0440 1", "price": "90 \u043b\u0432.", "image_url": "https://frankfurt.apollo.olxcdn.com:443/v1/files/r0ifq2q90ha92-BG/image;s=800x600", "description": "\u041d\u043e\u0432\u0430 \u0441 \u0435\u0442\u0438\u043a\u0435\u0442\u0438\u0442\u0435, \u0446\u0435\u043d\u0430 \u043f\u043e \u0435\u0442\u0438\u043a\u0435\u0442 159 \u043f\u0430\u0443\u043d\u0434\u0430", "upload_time": 1234567812}
        print(doc['title'])
        self._es.index('ads', body=doc, id=doc['url'])


if __name__ == '__main__':
    repository = AdItemRepository()
