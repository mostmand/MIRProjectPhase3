import scrapy

from crawler.classes.document import Document
from crawler.classes.json_serializer import JSONSerializer
from selenium import webdriver

distinct_titles = set()


class DigikalaSpider(scrapy.Spider):
    name = "digikala"

    def start_requests(self):
        self.n = int(self.n)
        self.browser = webdriver.Firefox()
        urls = [
            'https://www.digikala.com/product/dkp-173097/تبلت-ایسوس-مدل-zenpad-80-z380knl-4g-ظرفیت-16-گیگابایت/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self_url = '/' + '/'.join(response.url.split("/")[3:])
        title = response.css('.c-product__title::text').extract()[0].strip()

        if title in distinct_titles:
            return

        if len(distinct_titles) >= self.n:
            return
        distinct_titles.add(title)

        category = response.css('.c-breadcrumb').xpath('./li/a/span/text()')[3].extract().strip()
        expert_summary = response.css('.c-mask__text--product-summary').xpath('./p/text()').extract_first()
        expert_ratings = response.css('.c-content-expert__rating').xpath('./li')
        ratings = []
        for item in expert_ratings:
            expert_rating = item.xpath('./div')
            criteria = expert_rating[0].xpath('./text()').extract_first()
            rate = expert_rating[1].xpath('./div/@data-rate-digit').extract_first()
            rating = {'criteria': criteria, 'rating': rate}
            ratings.append(rating)

        self.browser.get(response.url)
        related_products = self.browser.find_elements_by_xpath("//div[@class='swiper-wrapper']/div/a")[0:5]

        urls = []
        relative_urls = []
        for related_product in related_products:
            url = related_product.get_attribute('href')
            urls.append(url)
            relative_url = '/' + '/'.join(url.split('/')[3:])
            relative_urls.append(relative_url)

        document = Document()
        document.title = title
        document.url = self_url
        document.category = category
        if expert_summary is not None:
            document.expert_summary = expert_summary.strip()
        if len(ratings) > 0:
            document.expert_rating = ratings
        document.related_product = relative_urls

        json = JSONSerializer.serialize(document)
        filename = 'jsons/digikala-%s.json' % title
        with open(filename, 'w') as f:
            f.write(json)

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def close_spider(self, spider):
        self.browser.close()

