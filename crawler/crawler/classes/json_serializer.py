import json


class JSONSerializer:
    @staticmethod
    def serialize(doc):
        return json.dumps(doc.__dict__, ensure_ascii=False)
