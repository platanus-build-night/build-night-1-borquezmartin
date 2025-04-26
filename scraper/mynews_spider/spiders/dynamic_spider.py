import scrapy
import datetime
from dynamic_scraper import scrap_dynamic_async

class DynamicSpider(scrapy.Spider):
    name = "dynamic_scraper"
    def __init__(self, url=None, portal='the_guardian', article_type='article', limit=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not url:
            raise ValueError("Debes pasar el parámetro `url` al spider")
        self.start_url     = url
        self.portal        = portal
        self.article_type  = article_type
        self.limit         = int(limit)

        # Prepara batch_id y contador
        today = datetime.datetime.now().strftime("%Y%m%d")
        self.batch_id     = f"{self.portal}_{today}"
        self.news_counter = 0

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    async def parse(self, response):
        # Llama a tu función asíncrona
        items = await scrap_dynamic_async(
            url=self.start_url,
            portal=self.portal,
            article_type=self.article_type,
            limit=self.limit
        )

        for entry in items:
            self.news_counter += 1
            yield {
                "batch_id": self.batch_id,
                "batch_data": {
                    "news_id": self.news_counter,
                    "title": entry["title"],
                    "url": entry["url"],
                    "description": entry["description"],
                    "portal": self.portal
                    }
                }

# import scrapy
# from dynamic_scraper import scrap_dynamic_async

# class DynamicSpider(scrapy.Spider):
#     name = "dynamic_scraper"
#     # permite pasar parámetros por línea de comando
#     def __init__(self, url=None, portal='guardian', article_type='article', limit=10, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if not url:
#             raise ValueError("Debes pasar el parámetro `url` al spider")
#         self.start_url     = url
#         self.portal        = portal
#         self.article_type  = article_type
#         self.limit         = int(limit)

#     def start_requests(self):
#         yield scrapy.Request(self.start_url, callback=self.parse)

#     async def parse(self, response):
#         items = await scrap_dynamic_async(
#             url=self.start_url,
#             portal=self.portal,
#             article_type=self.article_type,
#             limit=self.limit
#         )
#         for entry in items:
#             yield entry
            
#     # def parse(self, response):
#     #     # ignoramos response y usamos directamente tu función
#     #     results = scrap_dynamic_async(
#     #         url=self.start_url,
#     #         portal=self.portal,
#     #         article_type=self.article_type,
#     #         limit=self.limit
#     #     )
#     #     for entry in results:
#     #         yield entry
