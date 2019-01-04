from typing import Dict


class IdsManager:
    id_to_url_dic: Dict[int, str] = {}
    url_to_id_dic: Dict[str, int] = {}
    first_available_id: int = 1

    def assign_new_id(self) -> int:
        self.first_available_id += 1
        return self.first_available_id - 1

    def get_id_by_url(self, url: str) -> int:
        if url not in self.url_to_id_dic:
            page_id = self.assign_new_id()
            self.url_to_id_dic[url] = page_id
            self.id_to_url_dic[page_id] = url
        return self.url_to_id_dic[url]

    def get_url_by_id(self, page_id):
        if page_id in self.id_to_url_dic:
            return self.id_to_url_dic[page_id]

    def contains_id(self, page_id):
        return page_id in self.id_to_url_dic

    def contains_url(self, url):
        return url in self.url_to_id_dic
