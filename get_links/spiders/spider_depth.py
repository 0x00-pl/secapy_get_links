from urllib.parse import urlparse
import scrapy

__author__ = 'pl'


class MySpider(scrapy.Spider):
    name = "getall"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com/",
    ]
    results = None

    @staticmethod
    def result_from_url_parsed(url_parsed):
        return url_parsed.scheme + "://" + url_parsed.netloc

    def add_result(self, url_parsed):
        result = self.result_from_url_parsed(url_parsed)
        self.results.add(result)

    def link_filter(self, url_parsed):
        if not url_parsed.netloc.endswith(self.allowed_domains[0]):
            return False
        if self.result_from_url_parsed(url_parsed) in self.results:
            return False
        return True

    def parse(self, response):
        try:
            hxs = scrapy.Selector(response)
            # extract all links from page
            all_links = hxs.xpath('*//@href').extract()
            all_links = set(all_links)
        except Exception:
            return
        # iterate over links
        for link in all_links:
            next_page = response.urljoin(link)
            url_parsed = urlparse(next_page)
            if self.link_filter(url_parsed):
                self.add_result(url_parsed)
                yield scrapy.Request(next_page, callback=self.parse)


def normallize_start_urls(start_urls):
    if type(start_urls) != list:
        start_urls = [start_urls]
    return start_urls


def normallize_allowed_domains(allowed_domains, start_urls):
    if allowed_domains is None:
        netlocs = [urlparse(i).netloc for i in start_urls]
        netlocs = set(netlocs)
        allowed_domains = list(netlocs)

    if type(allowed_domains) != list:
        allowed_domains = [allowed_domains]
    return allowed_domains


def main(start_urls, depth, allowed_domains=None, pipe=None):
    from scrapy.crawler import CrawlerProcess, CrawlerRunner
    start_urls = normallize_start_urls(start_urls)
    allowed_domains = normallize_allowed_domains(allowed_domains, start_urls)

    results = set()

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DEPTH_LIMIT': depth,
        'DOWNLOAD_TIMEOUT': 10,
        'LOG_ENABLED': False
    })

    process.crawl(MySpider, start_urls=start_urls, allowed_domains=allowed_domains, results=results)
    process.start()
    process.stop()

    # [print(i)for i in MyPipeline.results]
    # print(len(MyPipeline.results))
    ret = list(results)
    if pipe is not None:
        pipe.send(ret)
    return ret


def main_with_process(start_urls, depth, allowed_domains=None):
    from multiprocessing import Process, Pipe

    recv_end, send_end = Pipe(False)
    p = Process(target=main, args=[start_urls, depth, allowed_domains, send_end])
    p.start()
    p.join()
    ret = recv_end.recv()

    return ret


if __name__ == "__main__":
    res = main_with_process(["http://www.baidu.com"], 2, ["baidu.com"])
    [print(i) for i in res]
    print("length:", len(res))
