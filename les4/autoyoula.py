import scrapy
import pymongo


class AutoyuolaSpider(scrapy.Spider):
    name = "autoyuola"
class AutoyoulaSpider(scrapy.Spider):
    name = "autoyoula"
    allowed_domains = ["auto.youla.ru"]
    start_urls = ["https://auto.youla.ru/"]

    css_query = {
        "brands": "div.TransportMainFilters_brandsList__2tIkv div.ColumnItemList_container__5gTrc a.blackLink",
        "brands": "div.TransportMainFilters_block__3etab a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "ads": "div.SerpSnippet_titleWrapper__38bZM a.blackLink",
        "ads": "article.SerpSnippet_snippet__3O1t2 a.blackLink",
    }

    data_query = {
        "title": "div.AdvertCard_advertTitle__1S1Ak::text",
        "price": "div.AdvertCard_price__3dDCr::text",
        "description": "div.AdvertCard_descriptionInner__KnuRi::text",
        "title": lambda resp: resp.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
        "price": lambda resp: float(resp.css('div.AdvertCard_price__3dDCr::text').get().replace("\u2009", '')),
    }

    @staticmethod
    def gen_tasks(response, link_list, callback):
        for link in link_list:
            yield response.follow(link.attrib.get("href"), callback=callback)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def parse(self, response):
        yield from self.gen_tasks(
            response, response.css(self.css_query["brands"]), self.brand_parse
        )
    def parse(self, response, **kwargs):
        brands_links = response.css(self.css_query["brands"])
        yield from self.gen_task(response, brands_links, self.brand_parse)

    def brand_parse(self, response):
        yield from self.gen_tasks(
            response, response.css(self.css_query["pagination"]), self.brand_parse
        )
        yield from self.gen_tasks(response, response.css(self.css_query["ads"]), self.ads_parse)
        pagination_links = response.css(self.css_query["pagination"])
        yield from self.gen_task(response, pagination_links, self.brand_parse)
        ads_links = response.css(self.css_query["ads"])
        yield from self.gen_task(response, ads_links, self.ads_parse)

    def ads_parse(self, response):
        data = {}
        for key, query in self.data_query.items():
            data[key] = response.css(query).get()
        for key, selector in self.data_query.items():
            try:
                data[key] = selector(response)
            except (ValueError, AttributeError):
                continue
        self.db_client['gb_parse_12_01_2021'][self.name].insert_one(data)

    @staticmethod
    def gen_task(response, link_list, callback):
        for link in link_list:
            yield response.follow(link.attrib["href"], callback=callback)

