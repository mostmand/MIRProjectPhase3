from typing import List, Dict
from page_ranking.elastic_reader import ElasticReader
from page_ranking.ids_manager import IdsManager


class PageRanker:
    def __init__(self, elastic_address, index_name):
        self.elastic_address = elastic_address
        self.index_name = index_name

    def rank_pages(self, alpha, teleportation_rate):
        ids_manager = IdsManager()
        matrix_calculator = MatrixCalculator(alpha, teleportation_rate, ids_manager)
        for page in ElasticReader.read_pages(self.elastic_address, self.index_name):
            matrix_calculator.add_page(page)
        matrix = matrix_calculator.get_matrix()



class MatrixCalculator:
    pages: Dict[str, Dict[str, float]]

    def __init__(self, alpha, teleportation_rate, ids_manager: IdsManager):
        self.ids_manager: IdsManager = ids_manager
        self.teleportation_rate = teleportation_rate
        self.alpha = alpha
        self.pages = {}

    def add_page(self, page_dict: Dict):
        this_page_url: str = page_dict['url']
        if this_page_url not in self.pages:
            self.pages[this_page_url] = {}

        self.ids_manager.get_id_by_url(this_page_url)

        self.pages[this_page_url][this_page_url] = 1 - self.alpha

        related_count = len(page_dict['related_product'])

        for link in page_dict['related_product']:
            related_url = link.replace('https://www.digikala.com', '', 1)
            self.ids_manager.get_id_by_url(related_url)
            self.pages[this_page_url][related_url] = self.alpha * (1 - self.teleportation_rate) / related_count

    def get_matrix(self):
        processed_pages = self.pages.keys()
        all_seen_pages = self.ids_manager.url_to_id_dic.keys()

        for row_page in all_seen_pages:
            if row_page in processed_pages:
                not_linked_pages_count = len(all_seen_pages) - len(self.pages[row_page])
                for column_page in all_seen_pages:
                    if column_page not in self.pages[row_page].keys():
                        self.pages[row_page][column_page] = self.alpha * self.teleportation_rate / not_linked_pages_count
            else:
                self.pages[row_page] = {}
                for column_page in all_seen_pages:
                    if row_page == column_page:
                        self.pages[row_page][column_page] = 1 - self.alpha
                    else:
                        self.pages[row_page][column_page] = self.alpha / (len(all_seen_pages) - 1)

        matrix = [[0.0 for i in range(len(all_seen_pages))] for x in range(len(all_seen_pages))]
        for row_page in self.pages.keys():
            row_id = self.ids_manager.get_id_by_url(row_page)
            for column_page in self.pages[row_page].keys():
                column_id = self.ids_manager.get_id_by_url(column_page)
                matrix[row_id][column_id] = self.pages[row_page][column_page]

        return matrix


PageRanker('http://localhost:9200', 'test-index3').rank_pages(0.85, 0.1)
