import scrapy
from urllib.parse import urlparse



class MyntraSpider(scrapy.Spider):
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

