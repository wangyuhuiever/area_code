import scrapy
from area_code.items import ErrorItem, ProvinceItem, CityItem, CountyItem, TownItem, VillageItem


class AreaCodeSpider(scrapy.Spider):
    name = 'area_code'
    # allowed_domains = ['example.com']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm']

    def parse(self, response):
        content_list = response.css('.center_list_contlist li')
        latest = content_list[0]
        latest_url = latest.css('a::attr(href)').get()
        yield response.follow(latest_url, callback=self.parse_province)

    def parse_province(self, response):
        try:
            province_list = response.css('.provincetr td')
            for province in province_list:
                province_url = province.css('a::attr(href)').get()
                province_name = province.css('a::text').get()
                province_code = province_url.split('.')[0]
                yield ProvinceItem(
                    code=province_code,
                    name=province_name
                )
                if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_PROVINCE']:
                    yield response.follow(province_url, callback=self.parse_city)
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_city(self, response):
        try:
            city_list = response.css('.citytr')
            for city in city_list:
                data = city.css('a::text').getall()
                city_name = data[1] if data else None
                city_url = city.css('a::attr(href)').get()
                code_string = city_url.split('.')[0]
                city_code = code_string.split('/')[1]
                yield CityItem(
                    code=city_code,
                    name=city_name
                )
                if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_CITY']:
                    yield response.follow(city_url, callback=self.parse_county)
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_county(self, response):
        try:
            county_list = response.css('.countytr')
            for county in county_list:
                data = county.css('a::text').getall()
                # 如果没有a标签，则不会有data，就不继续进行了爬虫了。市辖区
                # 但是要将市辖区保存下来
                if data:
                    county_name = data[1] if data else None
                    county_url = county.css('a::attr(href)').get()
                    code_string = county_url.split('.')[0]
                    county_code = code_string.split('/')[1]
                    yield CountyItem(
                        code=county_code,
                        name=county_name
                    )
                    if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_COUNTY']:
                        yield response.follow(county_url, callback=self.parse_town)
                else:
                    data = county.css('td::text').getall()
                    county_code = data[0][:6]
                    county_name = data[1]
                    yield CountyItem(
                        code=county_code,
                        name=county_name
                    )
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_town(self, response):
        try:
            town_list = response.css('.towntr')
            for town in town_list:
                data = town.css('a::text').getall()
                if data:  # 如果没有a标签，则不会有data，就不继续进行了。比如直辖市
                    town_name = data[1] if data else None
                    town_url = town.css('a::attr(href)').get()
                    code_string = town_url.split('.')[0]
                    town_code = code_string.split('/')[1]
                    yield TownItem(
                        code=town_code,
                        name=town_name
                    )
                    if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_TOWN']:
                        yield response.follow(town_url, callback=self.parse_village)
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_village(self, response):
        try:
            village_list = response.css('.villagetr')
            for village in village_list:
                data = village.css('td::text').getall()
                if data:
                    code, type, name = data
                    yield VillageItem(
                        code=code,
                        name=name,
                        type=type
                    )
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )