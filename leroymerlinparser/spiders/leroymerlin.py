import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroymerlinparser.items import LeroymerlinparserItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://habarovsk.leroymerlin.ru/search/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@data-qa-product]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('main_price',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='primary-price']/span[@slot='price']/text() |"
                         " //div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='primary-price']/span[@slot='fract']/text() ")
        loader.add_xpath('main_currency',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='primary-price']/span[@slot='currency']/text()")
        loader.add_xpath('main_unit',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='primary-price']/span[@slot='unit']/text()")
        loader.add_xpath('area_price',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='primary-price']/span[@slot='price']/text() |"
                         " //div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='second-price']/span[@slot='fract']/text() ")
        loader.add_xpath('area_currency',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='second-price']/span[@slot='currency']/text()")
        loader.add_xpath('area_unit',
                         "//div[contains(@data-testid, 'prices_mf-pdp')]/showcase-price-view[@slot='second-price']/span[@slot='unit']/text()")
        loader.add_xpath('photos', "//picture[@slot='pictures']/img/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('features', "//dl/div")
        yield loader.load_item()
