from typing import List, Dict


class Document:
    title: str
    url: str
    category: str
    expert_summary: str
    expert_rating: List[Dict[str, str]]
    related_product: List[str]

