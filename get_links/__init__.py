from .spiders import get_links


def simple_get(start_urls, allowed_domains=None):
    get_links.main(start_urls, allowed_domains)
