from elasticsearch import Elasticsearch


def search(elastic_address, index_name, must, must_not, should):
    client = Elasticsearch(elastic_address)


