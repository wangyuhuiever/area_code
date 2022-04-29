import scrapy
from area_code.items import ErrorItem, ProvinceItem, CityItem, CountyItem, TownItem, VillageItem


class AreaCodeSpider(scrapy.Spider):
    name = 'area_code'
    # allowed_domains = ['example.com']
    # start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm']
    start_urls = ['http://localhost:5000/api/auth']

    def parse(self, response):
        content_list = response.css('.center_list_contlist li')
        years = self.settings['YEARS']
        if not years:
            latest = content_list[0]
            year = latest.css('.cont_tit03::text').get()
            latest_url = latest.css('a::attr(href)').get()
            yield response.follow(latest_url, callback=self.parse_province, meta={'year': year})
        else:
            for content in content_list:
                year = content.css('.cont_tit03::text').get()
                if 'all' in years or year in years:  # 如果列表中有all，则全部爬取
                    url = content.css('a::attr(href)').get()
                    if url:  # 有可能url为none
                        yield response.follow(url, callback=self.parse_province, meta={'year': year})

    def parse_province(self, response):
        year = response.meta.get('year')
        try:
            province_list = response.css('.provincetr td')
            for province in province_list:
                province_url = province.css('a::attr(href)').get()
                province_name = province.css('a::text').get()
                province_code = province_url.split('.')[0]
                yield ProvinceItem(
                    code=province_code,
                    name=province_name,
                    year=year
                )
                if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_PROVINCE']:
                    yield response.follow(province_url, callback=self.parse_city, meta={'year': year})
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_city(self, response):
        year = response.meta.get('year')
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
                    name=city_name,
                    year=year
                )
                if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_CITY']:
                    yield response.follow(city_url, callback=self.parse_county, meta={'year': year})
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_county(self, response):
        year = response.meta.get('year')
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
                        name=county_name,
                        year=year
                    )
                    if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_COUNTY']:
                        yield response.follow(county_url, callback=self.parse_town, meta={'year': year})
                else:
                    data = county.css('td::text').getall()
                    county_code = data[0][:6]
                    county_name = data[1]
                    yield CountyItem(
                        code=county_code,
                        name=county_name,
                        year=year
                    )
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_town(self, response):
        year = response.meta.get('year')
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
                        name=town_name,
                        year=year
                    )
                    if self.settings['LEVEL_SPIDER'] > self.settings['LEVEL_TOWN']:
                        yield response.follow(town_url, callback=self.parse_village, meta={'year': year})
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )

    def parse_village(self, response):
        year = response.meta.get('year')
        try:
            village_list = response.css('.villagetr')
            for village in village_list:
                data = village.css('td::text').getall()
                if data:
                    code, type, name = data
                    yield VillageItem(
                        code=code,
                        name=name,
                        type=type,
                        year=year
                    )
        except Exception as e:
            self.logger.error(e)
            yield ErrorItem(
                url=response.url,
                message=str(e)
            )