from scrapy import cmdline


def crawl():
    n = 1000
    cmdline.execute("scrapy crawl digikala -a n={0}".format(n).split())
