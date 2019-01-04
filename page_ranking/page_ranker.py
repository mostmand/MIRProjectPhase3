from typing import List, Dict
from page_ranking.elastic_reader import ElasticReader
from page_ranking.ids_manager import IdsManager
import numpy


class PageRanker:
    def __init__(self, elastic_address, index_name):
        self.elastic_address = elastic_address
        self.index_name = index_name

    def rank_pages(self, alpha, teleportation_rate):
        ids_manager = IdsManager()
        matrix_calculator = MatrixCalculator(alpha, teleportation_rate, ids_manager)
        for page in ElasticReader.read_pages(self.elastic_address, self.index_name):
            matrix_calculator.add_page(page)
        (matrix, available_pages) = matrix_calculator.get_matrix()
        x = [0.0 for i in range(len(matrix))]
        first_page_id = ids_manager.get_id_by_url('/product/dkp-173097/%D8%AA%D8%A8%D9%84%D8%AA-%D8%A7%DB%8C%D8%B3%D9%88%D8%B3-%D9%85%D8%AF%D9%84-zenpad-80-z380knl-4g-%D8%B8%D8%B1%D9%81%DB%8C%D8%AA-16-%DA%AF%DB%8C%DA%AF%D8%A7%D8%A8%D8%A7%DB%8C%D8%AA')
        x[first_page_id] = 1

        x = numpy.array(x)

        max_iterations = 100
        error_tolerance = 1e-6

        for _ in range(max_iterations):
            last_x = x
            x = numpy.matmul(x, matrix)
            error = sum([abs(x[i] - last_x[i]) for i in range(len(x))])
            if error < len(matrix) * error_tolerance:
                break

        page_ranks = {}
        for available_url in available_pages:
            available_url_id = ids_manager.get_id_by_url(available_url)
            page_ranks[available_url] = x[available_url_id]

        for (url, page_rank) in page_ranks.items():
            ElasticReader.update_page_rank(self.elastic_address, self.index_name, url, page_rank)


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
        processed_pages = list(self.pages.keys())
        all_seen_pages = list(self.ids_manager.url_to_id_dic.keys())

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

        return numpy.array(matrix), processed_pages
