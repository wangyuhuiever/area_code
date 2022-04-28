# -*- coding: utf-8 -*-
import json
import sys
import operator
from area_code.mongo import MongoClient
from bson2json import format_pure_json

client = MongoClient()


def format_write_string(dic):
    string = json.dumps(dic, ensure_ascii=False)
    string += '\n'
    return string


def get_table(table_name):
    return client.get_collection(table_name)


def get_data(table_name):
    table = get_table(table_name)
    records = table.find().sort([('code', 1)])
    return list(map(format_pure_json, records))


def filter_code(code, data):
    res = list(filter(lambda f: f.get('code') == code, data))
    return res[0] if res else {}


def get_province_data():
    province_data = get_data('province')
    data = []
    for province in province_data:
        data.append({
            'code': province.get('code'),
            'province': province.get('name')
        })
    return data


def get_city_data():
    province_data = get_data('province')
    city_data = get_data('city')
    data = []
    for city in city_data:
        province_code = city.get('code')[:2]
        province = filter_code(province_code, province_data)
        data.append({
            'code': city.get('code'),
            'province': province.get('name'),
            'city': city.get('name'),
        })
    return data


def get_county_data(with_city=False):
    city_data = get_city_data()
    county_data = get_data('county')
    data = []
    for county in county_data:
        city_code = county.get('code')[:4]
        city = filter_code(city_code, city_data)
        data.append({
            'code': county.get('code'),
            'province': city.get('province'),
            'city': city.get('city'),
            'county': county.get('name'),
        })
    if with_city:
        for city in city_data:
            data.append({
                'code': city.get('code').ljust(6, '0'),
                'province': city.get('province'),
                'city': city.get('city'),
                'county': None
            })
    data = sorted(data, key=operator.itemgetter('code'))
    return data


def get_town_data():
    county_data = get_county_data()
    town_data = get_data('town')
    data = []
    for town in town_data:
        county_code = town.get('code')[:6]
        county = filter_code(county_code, county_data)
        data.append({
            'code': town.get('code'),
            'province': county.get('province'),
            'city': county.get('city'),
            'county': county.get('county'),
            'town': town.get('name'),
        })
    return data


def get_village_data():
    town_data = get_town_data()
    village_data = get_data('village')
    data = []
    for village in village_data:
        town_code = village.get('code')[:9]
        town = filter_code(town_code, town_data)
        data.append({
            'code': village.get('code'),
            'province': town.get('province'),
            'city': town.get('city'),
            'county': town.get('county'),
            'town': town.get('town'),
            'village': village.get('name'),
            'type': village.get('type'),
        })
    return data


def save_jsonl(table, with_city=False):
    if table == 'county':
        data = eval(f'get_{table}_data')(with_city)
    else:
        data = eval(f'get_{table}_data')()
    with open('result/area_code.jsonl', 'w') as file:
        file.writelines(map(format_write_string, data))


if __name__ == '__main__':
    level = sys.argv[1]
    try:
        county_with_city = sys.argv[2]
    except Exception as e:
        county_with_city = False
    level_list = ['province', 'city', 'county', 'town', 'village']
    if level not in level_list:
        print(f'请输入正确的level： {", ".join(level_list)}')
    else:
        save_jsonl(level, county_with_city)

