from setuptools import setup

__author__ = 'pl'

setup(
    name="get_links",
    version="0.5",
    packages=['get_links', 'get_links.spiders'],
    install_requires=['scrapy'],
    zip_safe=True,
)