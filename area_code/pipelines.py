# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from area_code.mongo import MongoClient


class AreaCodePipeline(object):

    def __init__(self):
        self.mongo = MongoClient()

    def process_item(self, item, spider):
        item.upsert()
        return item




