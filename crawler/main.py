import datetime
import os
from scrapy import cmdline
import indexing.indexer
import page_ranking.page_ranker


def crawl(n):
    path = 'jsons/' + str(datetime.datetime.now()) + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    cmdline.execute(['scrapy', 'crawl', 'digikala', '-a', 'n={0}'.format(n), '-a', 'path={0}'.format(path)])


def get_input_from_user():
    while True:
        print('Please select one of the options below:')
        print('1.Crawl')
        print('2.Remove elastic index')
        print('3.Index jsons into elastic')
        print('4.Calculate PageRank and index it into elastic')
        print('5.Search')
        print('0.Exit')
        inp = int(input())
        if inp == 0:
            break
        yield inp


jsons_path = 'jsons'
elastic_address = 'localhost:9200'
index_name = 'test-index3'

for inp in get_input_from_user():
    print(inp)
    if inp == 1:
        print('Please enter number of all pages to be crawled')
        n = int(input())
        crawl(n)
    elif inp == 2:
        indexing.indexer.remove_index(elastic_address, index_name)
    elif inp == 3:
        indexing.indexer.index(jsons_path, elastic_address, index_name)
    elif inp == 4:
        print('Please enter damping factor (alpha)')
        alpha = float(input())
        teleportation_rate = 0.1
        page_ranking.page_ranker.PageRanker(elastic_address, index_name).rank_pages(alpha, teleportation_rate)
    elif inp == 5:
        pass
    else:
        print('Your input is not recognized')
