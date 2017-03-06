from .spiders import spider_depth
from .spiders import get_links


def simple_get(start_urls, allowed_domains=None):
    return get_links.main_with_process(start_urls, allowed_domains)


def get_with_depth(start_urls, depth, allowed_domains=None):
    return spider_depth.main_with_process(start_urls, depth, allowed_domains)
