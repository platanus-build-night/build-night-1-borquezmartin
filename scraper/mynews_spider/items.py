# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MynewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):
    def __init__(self, title, url, description, news_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.url = url
        self.description = description
        self.news_type = news_type
    
    def __repr__(self):
        return super().__repr__()
    
