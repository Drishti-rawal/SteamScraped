# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose
from w3lib.html import remove_tags
from scrapy import Selector

def get_platforms(res):
    platforms = []
    platform = res.split(' ')[-1]
    if platform == 'win':
        platforms.append('windows')
    if platform == 'mac':
        platforms.append('Mac OS')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_supported':
        platforms.append('VR Supported')
    return platforms

def clean_discount(discount):
    if discount:
        return discount.lstrip('-')
    return discount

def get_original(html_obj):
    original_price=''
    obj=Selector(text=html_obj)
    discount_div=obj.xpath('.//div[contains(@class,"search_price discounted")]')
    if len(discount_div) > 0:
        original_price= discount_div.xpath('normalize-space(.//span/strike/text())').get()
    else:
        original_price=obj.xpath('normalize-space(.//div[contains(@class,"search_price")])').get()
    return (remove_tags(original_price))

class SteamItem(scrapy.Item):
    game_url=scrapy.Field(
        output_processor = TakeFirst()
    )
    platforms=scrapy.Field(
        input_processor=MapCompose(get_platforms),
    )
    img_url=scrapy.Field(
        output_processor=TakeFirst()
    )
    name=scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date=scrapy.Field(
        output_processor = TakeFirst()
    )
    review=scrapy.Field(
        input_processor = MapCompose(remove_tags),
        ouput_processor = TakeFirst()
    )
    original_price=scrapy.Field(
        input_processor = MapCompose(get_original)
    )
    rating=scrapy.Field()
    discounted_price=scrapy.Field(
        input_processor= MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    discount_rate=scrapy.Field(
        input_processor = MapCompose(clean_discount),
        output_processor=TakeFirst()
    )
