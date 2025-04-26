import scrapy
from dynamic_scraper import scrap_dynamic_async

class DynamicSpider(scrapy.Spider):
    name = "dynamic_scraper"
    # permite pasar parámetros por línea de comando
    def __init__(self, url=None, portal='guardian', article_type='article', limit=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not url:
            raise ValueError("Debes pasar el parámetro `url` al spider")
        self.start_url     = url
        self.portal        = portal
        self.article_type  = article_type
        self.limit         = int(limit)

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    async def parse(self, response):
        items = await scrap_dynamic_async(
            url=self.start_url,
            portal=self.portal,
            article_type=self.article_type,
            limit=self.limit
        )
        for entry in items:
            yield entry
            
    # def parse(self, response):
    #     # ignoramos response y usamos directamente tu función
    #     results = scrap_dynamic_async(
    #         url=self.start_url,
    #         portal=self.portal,
    #         article_type=self.article_type,
    #         limit=self.limit
    #     )
    #     for entry in results:
    #         yield entry
