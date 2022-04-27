import scrapy
from area_code.items import ProvinceItem, CityItem, CountyItem, TownItem, VillageItem


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
        province_list = response.css('.provincetr td')
        for province in province_list:
            province_url = province.css('a::attr(href)').get()
            province_name = province.css('a::text').get()
            province_code = province_url.split('.')[0]
            yield ProvinceItem(
                code=province_code,
                name=province_name
            )
            yield response.follow(province_url, callback=self.parse_city)

    def parse_city(self, response):
        city_list = response.css('.citytr')
        for city in city_list:
            data = city.css('a::text').getall()
            if data:  # 如果没有a标签，则不会有data，就不继续进行了。比如直辖市
                city_name = data[1] if data else None
                city_url = city.css('a::attr(href)').get()
                code_string = city_url.split('.')[0]
                city_code = code_string.split('/')[1]
                yield CityItem(
                    code=city_code,
                    name=city_name
                )
                yield response.follow(city_url, callback=self.parse_county)

    def parse_county(self, response):
        county_list = response.css('.countytr')
        for county in county_list:
            data = county.css('a::text').getall()
            if data:  # 如果没有a标签，则不会有data，就不继续进行了。比如直辖市
                county_name = data[1] if data else None
                county_url = county.css('a::attr(href)').get()
                code_string = county_url.split('.')[0]
                county_code = code_string.split('/')[1]
                yield CountyItem(
                    code=county_code,
                    name=county_name
                )
                yield response.follow(county_url, callback=self.parse_town)

    def parse_town(self, response):
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
                yield response.follow(town_url, callback=self.parse_village)

    def parse_village(self, response):
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
            