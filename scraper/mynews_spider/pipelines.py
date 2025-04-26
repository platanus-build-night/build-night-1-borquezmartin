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

# class JsonWriterPipeline:
#     def open_spider(self, spider):
#         self.file = open('articles.json', 'w', encoding='utf-8')
#         self.file.write('[')
#         self.first = True

#     def close_spider(self, spider):
#         self.file.write(']')
#         self.file.close()

#     def process_item(self, item, spider):
#         # item llega como dict
#         if not self.first:
#             self.file.write(',\n')
#         else:
#             self.first = False
#         line = json.dumps(dict(item), ensure_ascii=False)
#         self.file.write(line)
#         return item


# class BatchJsonWriterPipeline:
#     def open_spider(self, spider):
#         self.articles = []

#     def process_item(self, item, spider):
#         # item es {"batch_id": "...", "batch_data": {...}}
#         self.articles.append(item['batch_data'])
#         return item

#     def close_spider(self, spider):
#         output = {
#             "batch_id": spider.batch_id,
#             "batch_data": self.articles
#         }
#         with open("articles.json", "a", encoding="utf-8") as f:
#             json.dump(output, f, ensure_ascii=False, indent=5)

import os
import json

class BatchJsonWriterPipeline:
    def open_spider(self, spider):
        # Prepare in-memory list of this run’s articles
        self.articles = []
        # If the file doesn’t exist yet, create it as an empty JSON array
        if not os.path.exists("articles.json"):
            with open("articles.json", "w", encoding="utf-8") as f:
                f.write("[\n]")
    
    def process_item(self, item, spider):
        # Collect this batch’s data
        # item['batch_data'] is your dict for one article
        self.articles.append(item["batch_data"])
        return item

    def close_spider(self, spider):
        # Build the batch object
        batch = {
            "batch_id": spider.batch_id,
            "batch_data": self.articles
        }

        # Open the file for read+write, position at the end…
        with open("articles.json", "r+", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)
            # Step backwards, skipping any trailing whitespace, to find the last non-whitespace char
            pos = f.tell() - 1
            while pos > 0:
                f.seek(pos)
                char = f.read(1)
                if char not in (" ", "\n", "\r", "\t"):
                    break
                pos -= 1

            # Now `char` is the last non-ws character in the file.
            if char == "[":  # the array is empty: “[” … “]”
                # Move just after the “[” so we can insert our first element
                f.seek(pos + 1)
                f.truncate()
                f.write("\n")
            elif char == "]":
                # There was already at least one batch: remove the closing bracket
                f.seek(pos)
                f.truncate()
                f.write(",\n")
            else:
                # Unexpected—treat it as if the last element wasn’t closed by "]"
                f.seek(pos + 1)
                f.write(",\n")

            # Dump our new batch, then close the array
            json.dump(batch, f, ensure_ascii=False, indent=4)
            f.write("\n]")
