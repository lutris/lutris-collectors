"""Scraped items"""
import scrapy


class GOGProduct(scrapy.Item):
    """Item class for GOG products"""
    name = scrapy.Field()
    url = scrapy.Field()
    product_id = scrapy.Field()
    slug = scrapy.Field()
    product_type = scrapy.Field()
    access = scrapy.Field()
    supported_systems = scrapy.Field()
    developers = scrapy.Field()
    publisher = scrapy.Field()
    release_date = scrapy.Field()
    base_product = scrapy.Field()
    api_availability = scrapy.Field()
    last_updated = scrapy.Field()
