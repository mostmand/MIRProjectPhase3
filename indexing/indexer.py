import json
import os

from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index, Mapping, Keyword, Nested, Text, Double, Document


class Indexer:
    def __init__(self, elastic_address):
        self.client = Elasticsearch(hosts=elastic_address)

    def index(self, index_name, jsons_path):
        mapping = self.create_mapping()
        self.create_index(index_name, mapping)
        helpers.bulk(self.client, self.get_json_documents(jsons_path), index=index_name, doc_type='_doc')

    def create_index(self, index_name, mapping):
        index = Index(using=self.client, name=index_name)
        index.mapping(mapping)
        res = index.create()
        print(res)
        return index

    def remove_index(self, index_name):
        index = Index(using=self.client, name=index_name)
        index.delete()

    @staticmethod
    def create_mapping():
        mapping = Mapping(name='_doc')
        mapping.field('title', Text())
        mapping.field('url', Keyword())
        mapping.field('category', Text())
        mapping.field('expert_summary', Text())
        rating = Nested(
            properties={
                'criteria': Text(),
                'rating': Text()
            }, multi=True)
        mapping.field('expert_rating', rating)
        mapping.field('page_rank', Double())
        return mapping

    @staticmethod
    def get_json_documents(directory):
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.abspath(directory + '/' + filename)
                with open(file_path, 'r') as open_file:
                    yield json.load(open_file)


def index():
    jsons_path = 'jsons'
    elastic_address = 'localhost:9200'
    index_name = 'test-index3'
    remove_index(elastic_address, index_name)
    indexer = Indexer(elastic_address)
    indexer.index(index_name, jsons_path)


def remove_index(elastic_address, index_name):
    indexer = Indexer(elastic_address)
    indexer.remove_index(index_name)


