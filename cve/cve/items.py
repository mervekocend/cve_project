# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CveItem(scrapy.Item):
    CVE_ID = scrapy.Field()
    CWE_ID = scrapy.Field()
    VULNERABILITY_TYPE = scrapy.Field()
    PUBLISH_DATE = scrapy.Field()
    UPDATE_DATE = scrapy.Field()
    SCORE = scrapy.Field()
    SUMMARY = scrapy.Field()