from scrapy.spiders import Spider
from scrapy import Request
from play.items import PlayItem
import sqlite3

class metainfo(Spider):
    name = 'metainfo'  
    allowed_domains = ["play.google.com"]
    
    con = sqlite3.connect("databases/GooglePlayApps.db")
    cur = con.cursor()
    cur.execute("select packageName from applist;")
    appList = cur.fetchall()
    con.close()
    
    start_urls = ["https://play.google.com/store/apps/details?id="+ i[0] for i in appList]

    def parse(self,response):
        item = PlayItem()
        
        text = response.xpath('//span[@class = "bar-number"]/text()').extract()
        if text:
            rating5 = int(text[0].strip().replace(",", ""))
            rating4 = int(text[1].strip().replace(",", ""))
            rating3 = int(text[2].strip().replace(",", ""))
            rating2 = int(text[3].strip().replace(",", ""))
            rating1 = int(text[4].strip().replace(",", ""))
        else:
            rating5 = 0
            rating4 = 0
            rating3 = 0
            rating2 = 0
            rating1 = 0
        ratingDist = [str(rating5), str(rating4), str(rating3), str(rating2), str(rating1)]
        
        item["packageName"] = response.url.split("=")[1].strip()
        item["title"] = response.xpath('//div[@class = "id-app-title"]/text()').extract()[0].strip()
        item["datePublished"] = response.xpath('//div[@class = "meta-info"]/div[@itemprop = "datePublished"]/text()').extract()[0].strip()
        item["fileSize"] = 0 # response.xpath('//div[@class = "meta-info"]/div[@itemprop = "fileSize"]/text()').extract()[0].strip()
        item["numComments"] = rating5 + rating4 + rating3 + rating2 + rating1
         
        text = response.xpath('//div[@class = "meta-info"]/div[@itemprop = "numDownloads"]/text()').extract()
        if text:
            item["numDownloads"] = int(text[0].split("-")[1].strip().replace(",", ""))
        else:
            item["numDownloads"] = 0

        text = response.xpath('//div[@class = "meta-info"]/div[@itemprop = "softwareVersion"]/text()').extract()
        if text:
            item["softwareVersion"] = text[0].strip()
        else:
            item["softwareVersion"] = ""

        text = response.xpath('//div[@class = "meta-info"]/div[@itemprop = "operatingSystems"]/text()').extract()
        if text:
            item["operatingSystems"] = text[0].strip()
        else:
            item["operatingSystems"] = ""

        text = response.xpath('//div[@class = "meta-info contains-text-link"]/div[@itemprop = "contentRating"]/text()').extract()
        if text:
            item["contentRating"] = text[0].strip()
        else:
            item["contentRating"] = ""

        item["price"] = 0.0
        
        text = response.xpath('//div[@itemprop = "description"]/div[@jsname = "C4s9Ed"]/text()').extract()
        if text:
            item["description"] = " ".join(text).strip()
        else:
            item["description"] = ""

        text = response.xpath('//span[@itemprop = "name"]/text()').extract()
        if text:
            item["developer"] = text[0].strip()
        else:
            item["developer"] = ""

        try:
            item["devMail"] = response.xpath('//a[@class = "dev-link"]')[1].select("@href").extract()[0].split(":")[1].strip()
            item["devLink"] = response.xpath('//a[@class = "dev-link"]')[0].select("@href").extract()[0].strip()
        except:
            item["devMail"] = ""
            item["devLink"] = ""

        item["category"] = response.xpath('//a[@class = "document-subtitle category"]/span[@itemprop = "genre"]/text()').extract()[0].strip()
        item["categoryUrl"] = "https://play.google.com" + response.xpath('//a[@class = "document-subtitle category"]').select("@href").extract()[0].strip()
        
        text = response.xpath('//div[@class = "score-container-star-rating"]/div[@class = "small-star star-rating-non-editable-container"]/div[@class = "current-rating"]').select("@style").extract()
        if text:
            item["currentRating"] = float(text[0].split(":")[1].split("%")[0].strip())
        else:
            item["currentRating"] = 0.0
        
        item["distRating"] = ",".join(ratingDist)
        
        if item["numComments"]:
            item["avgRating"] = 1.0*(5*rating5 + 4*rating4 + 3*rating3 + 2*rating2 + rating1) / item["numComments"]
        else:
            item["avgRating"] = 0.0
        
        yield item
