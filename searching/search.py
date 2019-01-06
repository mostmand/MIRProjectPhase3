from typing import List

from elasticsearch import Elasticsearch

from searching.command import Command


def search(elastic_address, index_name, must: List[Command], must_not: List[Command], should: List[Command]):
    client = Elasticsearch(elastic_address)


