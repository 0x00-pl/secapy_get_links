import scrapy
from urllib.parse import urlparse


class MySpider(scrapy.Spider):
    name = "getall"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.sina.com/",
    ]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        all_links = set(all_links)
        # iterate over links
        for link in all_links:
            abs_link = response.urljoin(link)
            url_parsed = urlparse(abs_link)
            if url_parsed.netloc.endswith(self.allowed_domains[0]):
                yield {"link": abs_link, "netloc": url_parsed.netloc, "scheme": url_parsed.scheme}


class MyPipeline(object):
    results = set()

    def process_item(self, item, spider):
        self.results.add(dict(item)['netloc'])


def main(start_urls, allowed_domains=None):
    from scrapy.crawler import CrawlerProcess

    if allowed_domains is None:
        netlocs = [urlparse(i).netloc for i in start_urls]
        netlocs = set(netlocs)
        allowed_domains = list(netlocs)

    MyPipeline.results = set()

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'__main__.MyPipeline': 1},
        'LOG_ENABLED': False
    })

    process.crawl(MySpider, start_urls=start_urls, allowed_domains=allowed_domains)
    process.start()

    # [print(i)for i in MyPipeline.results]
    # print(len(MyPipeline.results))
    return list(MyPipeline.results)


if __name__ == "__main__":
    res = main(["http://www.baidu.com"], ["baidu.com"])
    [print(i) for i in res]
