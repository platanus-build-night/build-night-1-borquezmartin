# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class MynewsSpiderPipeline:
#     def process_item(self, item, spider):
#         return item

import json

class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('articles.json', 'w', encoding='utf-8')
        self.file.write('[')
        self.first = True

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        # item llega como dict
        if not self.first:
            self.file.write(',\n')
        else:
            self.first = False
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        return item
