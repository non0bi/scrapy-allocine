# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAllocineItem(scrapy.Item):
    # define the fields for your item:
    pass

class FilmItem(scrapy.Item):
    titre = scrapy.Field()
    note_spectateurs = scrapy.Field()
    note_presse = scrapy.Field()
    genre = scrapy.Field()
    duree = scrapy.Field()
    date_sortie = scrapy.Field()
    url = scrapy.Field()
