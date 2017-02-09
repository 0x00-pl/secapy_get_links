import scrapy
from urllib.parse import urlparse


class MySpider(scrapy.Spider):
    name = "getall"
    allowed_domains = ["4f61.com"]
    start_urls = [
        "http://www.4f61.com/",
    ]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        all_links = set(all_links)
        # iterate over links
        for link in all_links:
            abs_link = response.urljoin(link)
            if urlparse(abs_link).netloc.endswith(self.allowed_domains[0]):
                yield {"link": abs_link}


class MyPipeline(object):
    results = []

    def process_item(self, item, spider):
        MyPipeline.results.append(dict(item))


def main():
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'__main__.MyPipeline': 1},
        'LOG_ENABLED': False
    })

    process.crawl(MySpider)
    process.start()

    print(MyPipeline.results)


if __name__ == "__main__":
    main()
