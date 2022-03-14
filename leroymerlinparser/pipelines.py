# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroymerlinparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leruamerlin

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        link = item['url']
        if collection.count_documents({"lurl": link}) == 0:
            collection.insert_one(item)
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for photo in item['photos']:
                try:
                    yield scrapy.Request(photo)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):

        """Сохранение по папкам"""
        folder_name = item['name']
        image_name = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{folder_name}/{image_name}.jpg'
