import indexing.indexer
import page_ranking.page_ranker
from crawler import crawler


def get_input_from_user():
    while True:
        print('Please select one of the options below:')
        print('1.Crawl')
        print('2.Remove elastic index')
        print('3.Index jsons into elastic')
        print('4.Calculate PageRank and index it into elastic')
        print('5.Search')
        print('0.Exit')
        try:
            inp = int(input())
            if inp == 0:
                break
            yield inp
        except:
            print('Your input is not recognized')


jsons_path = 'jsons'
elastic_address = 'localhost:9200'
index_name = 'test-index3'

for inp in get_input_from_user():
    print(inp)
    if inp == 1:
        n = int(input('Please enter number of all pages to be crawled\n'))
        crawler.crawl(n)
    elif inp == 2:
        indexing.indexer.remove_index(elastic_address, index_name)
    elif inp == 3:
        indexing.indexer.index(jsons_path, elastic_address, index_name)
    elif inp == 4:
        alpha = float(input('Please enter damping factor (alpha)\n'))
        teleportation_rate = 0.1
        page_ranking.page_ranker.PageRanker(elastic_address, index_name).rank_pages(alpha, teleportation_rate)
    elif inp == 5:
        pass
