# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from area_code.mongo import MongoClient


class MongoMixin(object):
    mongo = MongoClient()

    def upsert(self):
        collection = self.mongo.get_collection(self._name)
        collection.update_one({'code': self['code'], 'year': self['year']}, {"$set": dict(self)}, upsert=True)


class ErrorItem(scrapy.Item, MongoMixin):
    _name = 'error'

    url = scrapy.Field()
    message = scrapy.Field()

    def upsert(self):
        collection = self.mongo.get_collection(self._name)
        collection.update_one({'url': self['url']}, {"$set": dict(self)}, upsert=True)


class ProvinceItem(scrapy.Item, MongoMixin):
    _name = 'province'

    code = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()


class CityItem(scrapy.Item, MongoMixin):
    _name = 'city'

    code = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()


class CountyItem(scrapy.Item, MongoMixin):
    _name = 'county'

    code = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()


class TownItem(scrapy.Item, MongoMixin):
    _name = 'town'

    code = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()


class VillageItem(scrapy.Item, MongoMixin):
    _name = 'village'

    code = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()

