from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class ElasticReader:
    @staticmethod
    def read_pages(elastic_address, index_name):
        client = Elasticsearch(elastic_address)
        search = Search(using=client, index=index_name).source(fields=['url', 'related_product'])
        total = search.count()
        search = search[0:total]
        results = search.execute()
        for result in results.hits.hits:
            yield result['_source']


# iterator = ElasticReader.read_pages('http://localhost:9200', 'test-index3').__iter__()
# counter = 0
# while counter < 10:
#     print(iterator.__next__())
#     counter += 1
