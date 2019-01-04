from scrapy import cmdline
import datetime


def crawl(n):
    path = 'josns/' + str(datetime.datetime.now()) + '/'
    cmdline.execute("scrapy crawl digikala -a n={0} -path={1}".format(n, path).split())
