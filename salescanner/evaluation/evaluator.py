import json
import re
from salescanner.repositories.ad_index_template import AdIndexTemplate
from salescanner.repositories.ad_item_repository import AdItemRepository
from salescanner.services.ad_item_service import AdItemService

from elasticsearch import helpers


class Evaluator:

    EVALUATION_INDEX = 'evaluate'
    ANNOTED_ADS_PATH = 'ads_json/annotated_ads.json'

    @staticmethod
    def evaluate():
        with open(Evaluator.ANNOTED_ADS_PATH, 'r') as ads_file:
            ads = json.load(ads_file)

        Evaluator._bulk_into_es(ads)
        Evaluator._evaluate_literacy(ads)
        Evaluator._evaluate_search_precision_recall(ads)
        es = AdItemRepository._get_connection()
        es.indices.delete(Evaluator.EVALUATION_INDEX)

    @staticmethod
    def _bulk_into_es(ads):
        es = AdItemRepository._get_connection()
		
        if es.indices.exists(Evaluator.EVALUATION_INDEX):
            es.indices.delete(Evaluator.EVALUATION_INDEX)
        es.indices.create(Evaluator.EVALUATION_INDEX, body=AdIndexTemplate.get_index_mapping())
			
        actions = [
            {
                "_index": Evaluator.EVALUATION_INDEX,
                "_id": ad['url'],
                "_source": ad
            }
            for ad in ads
        ]
        helpers.bulk(es, actions)
        es.indices.refresh(Evaluator.EVALUATION_INDEX)
        print(f'{len(ads)} ads inserted into ElasticSearch evaluation index')

    @staticmethod
    def _evaluate_literacy(ads):
        correctly_scored = 0
        for ad in ads:
            literacy_score = AdItemService.calculate_literacy_score(ad)
            if literacy_score >= 70 and ad['high_literacy']:
                correctly_scored += 1
            if literacy_score < 70 and not ad['high_literacy']:
                correctly_scored += 1
        
        accuracy = correctly_scored / len(ads)
        print('##################### LITERACY #####################')
        print(f'Accuracy: {accuracy}')
        print('####################### END ########################\n\n')

    @staticmethod
    def _evaluate_search_precision_recall(ads):
        print('###################### SEARCH ######################')
        topics = dict()
        for ad in ads:
            for topic in ad['topics']:
                topics[topic] = topics.get(topic, 0) + 1
        
        pairs = [pair for pair in topics.items()]
        pairs.sort(key=lambda pair: pair[1], reverse=True)
        print(f'Topics of interest: {pairs[0:3]}')

        topics_of_interest = pairs[0:3]
        overall_precision, overall_recall, overall_f1 = 0, 0, 0
        for topic in topics_of_interest:
            precision, recall, f1 = Evaluator._evaluate_topic_precision_recall(ads, topic)
            overall_precision += precision
            overall_recall += recall
            overall_f1 += f1

        overall_precision /= 3
        overall_recall /= 3
        overall_f1 /= 3
        print('\nOverall scores:')
        print(f'Precision: {overall_precision}')
        print(f'Recall: {overall_recall}')
        print(f'F1: {f1}')

        print('######################## END #######################')
    
    @staticmethod
    def _evaluate_topic_precision_recall(ads, topic_pair):
        topic, occurance = topic_pair
        
        es = AdItemRepository._get_connection()
        query = AdItemRepository.construct_query(topic, 'score', 0, 100)
        query_res = es.search(index=Evaluator.EVALUATION_INDEX, body=query)
        
        hits = [hit['_source'] for hit in query_res.get('hits', {}).get('hits', [])]
        query_correct_hits = [hit for hit in hits if topic in hit['topics']]
        all_correct_hits = [ad for ad in ads if topic in ad['topics']]

        precision = len(query_correct_hits) / len(hits)
        recall = len(query_correct_hits) / len(all_correct_hits)
        f1 = (2 * precision * recall) / (precision + recall)
        
        print(f'\nTopic "{topic}" scores:')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')
        print(f'F1: {f1}')
        
        return precision, recall, f1


if __name__ == '__main__':
    Evaluator.evaluate()
