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

    @staticmethod
    def update_page_rank(elastic_address, index_name, url, page_rank):
        client = Elasticsearch(elastic_address)

        search_body = {
            "query": {
                "bool": {
                    "filter": {
                        "term": {"url": '%s' % url}
                    }
                }
            }
        }
        doc_id = client.search(index=index_name, body=search_body)['hits']['hits'][0]['_id']

        update_body = {
            "doc": {
                "page_rank": page_rank
            }
        }

        update_response = client.update(index=index_name, doc_type='_doc', id=doc_id, body=update_body)
        pass


# iterator = ElasticReader.read_pages('http://localhost:9200', 'test-index3').__iter__()
# counter = 0
# while counter < 10:
#     print(iterator.__next__())
#     counter += 1
