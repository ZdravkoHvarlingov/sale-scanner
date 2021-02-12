import pytz

from salescanner.repositories.ad_index_template import AdIndexTemplate
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime, timedelta


class AdItemRepository:

	ADS_INDEX_NAME = 'ads'
	DEFAULT_ORDER_BY_ATTRIBUTE = '_score'
	DEFAULT_PAGE_SIZE = 20
	DEFAULT_EXPIRATION_DAYS = 7

	_es_connection = None

	@staticmethod
	def _get_connection():
		if AdItemRepository._es_connection is None:
			AdItemRepository._es_connection = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		
		if not AdItemRepository._es_connection.ping():
			raise ValueError("Connection failed")
		
		return AdItemRepository._es_connection
	
	@staticmethod
	def delete_old():
		es = AdItemRepository._get_connection()
		index_name = AdItemRepository.ADS_INDEX_NAME

		timezone = pytz.timezone('utc')
		min_datetime = datetime.utcnow() - timedelta(days=AdItemRepository.DEFAULT_EXPIRATION_DAYS)
		min_datetime = timezone.localize(min_datetime)
		min_timestamp = int(min_datetime.timestamp() * 1000)

		delete_query = {
			"query": {
				"range": {
					"upload_time": {
						"lt": min_timestamp
					}
				}
			}
		}

		deleted = es.delete_by_query(index=index_name, body=delete_query).get('total', 0)
		print(f'Deleted {deleted} old ads.')

	@staticmethod
	def insert_list(ad_list):
		AdItemRepository.delete_old()
		es = AdItemRepository._get_connection()
		index_name = AdItemRepository.ADS_INDEX_NAME
		
		if not es.indices.exists(index_name):
			es.indices.create(index_name, body=AdIndexTemplate.get_index_mapping())

		actions = [
            {
                "_index": index_name,
                "_id": ad['url'],
                "_source": ad
            }
            for ad in ad_list
        ]
		helpers.bulk(es, actions)
		print(f'{len(ad_list)} ads inserted into ElasticSearch')

	@staticmethod
	def _construct_query(query_string, order_attribute, page, page_size):
		if order_attribute not in {'_score', 'score', 'upload_time', 'literacy'}:
			raise ValueError("Invalid order by attribute")

		if order_attribute == 'score':
			order_attribute = '_score'
		
		query_template = {
			"track_scores": True,
			"sort": { 
				order_attribute: { "order": "desc" }
			},
			"from": page * page_size,
			"size": page_size,
			"query": {
				"bool": {
					"should": [{
							"match": {
								"title": query_string
							}
						},
						{
							"match": {
								"description": query_string
							}
						}
					]
				}
			}
		}

		return query_template

	@staticmethod
	def find_by_query(query_string, order_attribute=DEFAULT_ORDER_BY_ATTRIBUTE, page=0, page_size=DEFAULT_PAGE_SIZE):
		es = AdItemRepository._get_connection()

		query_template = AdItemRepository._construct_query(query_string, order_attribute, page, page_size)
		query_res = es.search(index=AdItemRepository.ADS_INDEX_NAME, body=query_template)
		result = {
			'took': query_res.get('took'),
			'max_score': query_res.get('hits', {}).get('max_score'),
			'hits': [{ 'source': hit['_source'], 'score': hit['_score'] } for hit in query_res.get('hits', {}).get('hits', [])]
		}
		
		return result
	
	@staticmethod
	def count_ads():
		es = AdItemRepository._get_connection()
		es.indices.refresh(AdItemRepository.ADS_INDEX_NAME)
		res = es.cat.count(AdItemRepository.ADS_INDEX_NAME, params={"format": "json"})

		if len(res) > 0:
			return int(res[0]['count'])
		return 0


if __name__ == '__main__':
	# print(AdItemRepository.count_ads())
	# AdItemRepository.insert_list([])
	AdItemRepository.delete_old()
