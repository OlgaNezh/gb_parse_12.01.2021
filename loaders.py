import re
from scrapy import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from items import HhruItem
from items import InstaItem
# from .items import AutoYoulaItem

# def get_autor(js_string):
#     re_str = re.compile(r"youlaId%22%2C%22([0-9|a-zA-Z]+)%22%2C%22avatar")
#     result = re.findall(re_str, js_string)
#     return f'https://youla.ru/user/{result[0]}' if result else None
#
#
# def get_specifications(itm):
#     tag = Selector(text=itm)
#     result = {tag.css('.AdvertSpecs_label__2JHnS::text').get(): tag.css(
#         '.AdvertSpecs_data__xK2Qx::text').get() or tag.css('a::text').get()}
#     return result
#
#
# def specifications_out(data: list):
#     result = {}
#     for itm in data:
#         result.update(itm)
#     return result


# class AutoYoulaLoader(ItemLoader):
#     default_item_class = AutoYoulaItem
#     title_out = TakeFirst()
#     url_out = TakeFirst()
#     description_out = TakeFirst()
#     autor_in = MapCompose(get_autor)
#     autor_out = TakeFirst()
#     specifications_in = MapCompose(get_specifications)
#     specifications_out = specifications_out

def get_companyname(header_string):
    return re.search(r'Вакансии компании (.*?) - работа в', header_string).group(1)


class HhruLoader(ItemLoader):
    default_item_class = HhruItem
    title_out = TakeFirst()
    url_out = TakeFirst()
    description_in = ''.join
    description_out = TakeFirst()
    salary_in = ''.join
    salary_out = TakeFirst()
    company_name_in = MapCompose(get_companyname)
    company_name_out = TakeFirst()
    company_website_out = TakeFirst()
    company_description_out = TakeFirst()
    company_tags = TakeFirst()


class InstaLoader(ItemLoader):
    default_item_class = InstaItem
    date_parse = TakeFirst()
    data = TakeFirst()
    image_urls = TakeFirst()