from .spiders import get_links


def simple_get(start_urls, allowed_domains=None):
    return get_links.main_with_process(start_urls, allowed_domains)
