# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PlayItem(scrapy.Item):
    packageName = scrapy.Field()
    title = scrapy.Field()
    datePublished = scrapy.Field()
    fileSize = scrapy.Field()
    numDownloads = scrapy.Field()
    numComments = scrapy.Field()
    softwareVersion = scrapy.Field()
    operatingSystems = scrapy.Field()
    contentRating = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    developer = scrapy.Field()
    devMail = scrapy.Field()
    devLink = scrapy.Field()
    category = scrapy.Field()
    categoryUrl = scrapy.Field()
    currentRating = scrapy.Field()
    distRating = scrapy.Field()
    avgRating = scrapy.Field()
