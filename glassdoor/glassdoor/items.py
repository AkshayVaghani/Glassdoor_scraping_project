# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_id = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    city_state = scrapy.Field()
    job_desc = scrapy.Field()
    company_rating = scrapy.Field()
    average_salary = scrapy.Field()
    post_date = scrapy.Field()
    company_info = scrapy.Field()
    country_name = scrapy.Field()
