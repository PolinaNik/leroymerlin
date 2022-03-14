# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose
from bs4 import BeautifulSoup


def fix_price(price_list):
    try:
        if len(price_list) == 1:
            price = int(price_list[0].replace('\xa0', ''))
            return price
        else:
            price = int(price_list[0].replace('\xa0', ''))
            fract = int(price_list[1]) / 100
            price = price + fract
            return price
    except:
        return price_list


def feature_order(feature_list):
    try:
        features = {}
        for item in feature_list:
            dom = BeautifulSoup(item, 'html.parser')
            name_feature = dom.find('dt').getText()
            value_feature = dom.find('dd').getText()
            features[name_feature] = value_feature
        return features
    except:
        return feature_list


def unit_select(unit_list):
    try:
        return unit_list[1]
    except:
        return unit_list


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    main_price = scrapy.Field(input_processor=Compose(fix_price))
    main_currency = scrapy.Field(output_processor=TakeFirst())
    main_unit = scrapy.Field(input_processor=Compose(unit_select))
    area_price = scrapy.Field(input_processor=Compose(fix_price))
    area_currency = scrapy.Field(output_processor=TakeFirst())
    area_unit = scrapy.Field(input_processor=Compose(unit_select))
    photos = scrapy.Field()
    features = scrapy.Field(input_processor=Compose(feature_order))
    _id = scrapy.Field()
