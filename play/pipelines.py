# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import sqlite3

class Sqlite3Pipeline(object):

    def __init__(self, sqlite_file):
        self.sqlite_file = sqlite_file
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'), # extracted from settings.py
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        selectSQL = "select * from metainfo where packageName=\"{0}\";".format(item['packageName'])
        self.cur.execute(selectSQL)
        result = self.cur.fetchone()
        if result:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            insertSQL = "insert into metainfo (packageName, title, datePublished, fileSize, numDownloads, numComments, softwareVersion, operatingSystems, contentRating, price, description, developer, devMail, devLink, category, categoryUrl, currentRating, distRating, avgRating) values ({0});".format(', '.join(['?'] * len(item.fields.keys())))
            self.cur.execute(insertSQL, (item['packageName'], item['title'], item['datePublished'], item['fileSize'], item['numDownloads'], item['numComments'], item['softwareVersion'], item['operatingSystems'], item['contentRating'], item['price'], item['description'], item['developer'], item['devMail'], item['devLink'], item['category'], item['categoryUrl'], item['currentRating'], item['distRating'], item['avgRating']))
            self.conn.commit()
        return item
