# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

if __name__ == '__main__':
    spiders = ['area_code']
    for spider in spiders:
        process.crawl(spider)
    process.start()
