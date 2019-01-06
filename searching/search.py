import json
from typing import List
from elasticsearch import Elasticsearch


field_names = {'title', 'url', 'category', 'expert_rating', 'related_product', 'expert_summary', 'page_rank'}


def create_items(queries):
    items = []
    for query in queries:
        split = query.split('-')
        field_name = split[0].strip()
        value = split[1].strip()
        weight = 1.0
        if len(split) == 3:
            weight = float(split[2])
        if field_name in field_names:
            items.append({
                "match": {
                    "%s" % field_name: {
                        "query": "%s" % value,
                        "boost": weight
                    }
                }
            })
        else:
            items.append({
                "nested": {
                    "path": "expert_rating",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "expert_rating.criteria": {
                                            "query": "%s" % field_name,
                                            "boost": weight
                                        }
                                    }
                                },
                                {
                                    "match": {
                                        "expert_rating.rating": "%s" % value
                                    }
                                }
                            ]
                        }
                    }
                }
            })
    return items


def search(must_array: List[str], must_not_array: List[str], should_array: List[str]):
    index_name = 'test-index3'
    elastic_address = 'localhost:9200'
    must_items = create_items(must_array)
    must_not_items = create_items(must_not_array)
    should_items = create_items(should_array)

    search_body = {
        "query": {
            "bool": {
                "should": should_items,
                "filter": {
                    "bool": {
                        "must": must_items,
                        "must_not": must_not_items
                    }
                }
            },
            "sort": [
                {
                    "page_rank": {
                        "order": "desc"
                    }
                }
            ]
        }
    }
    client = Elasticsearch(elastic_address)
    response = client.search(index=index_name, body=search_body, doc_type='_doc')
    result = []
    for hit in response['hits']['hits']:
        result.append(json.dumps(hit, indent=4, sort_keys=True, ensure_ascii=False))

    return '\n'.join(result)


