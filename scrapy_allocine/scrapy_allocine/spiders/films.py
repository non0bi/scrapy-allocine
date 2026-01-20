import scrapy
from scrapy_allocine.items import FilmItem

class AllocineFilmsSpider(scrapy.Spider):
    name = "allocine_films"
    allowed_domains = ["allocine.fr"]
    start_urls = [
        "https://www.allocine.fr/film/aucinema/"
    ]

    def parse(self, response):
        # Sélection de tous les films de la page
        films = response.css("div.card.entity-card.entity-card-list")

        for film in films:
            item = FilmItem()

            # Infos de base
            item["titre"] = film.css("a.meta-title-link::text").get().strip()
            item["url"] = response.urljoin(
                film.css("a.meta-title-link::attr(href)").get()
            )
            item["note_spectateurs"] = film.css(
                "span.stareval-note::text"
            ).get()

            # On suit le lien pour scraper la page détail
            yield response.follow(
                item["url"],
                callback=self.parse_film,
                meta={"item": item}  # On transmet l'item pour le compléter
            )

        # Pagination
        next_page = response.css("a.button.button-md.button-primary-full::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_film(self, response):
        item = response.meta["item"]

        # Synopsis
        item["synopsis"] = response.css("div.content-txt::text").get(default="").strip()

        # Genre (liste)
        item["genre"] = response.css("span.dark-grey-link::text").getall()

        # Durée (ex: "1h42")
        item["duree"] = response.css("div.meta-body-item.meta-body-info::text").re_first(r"\d+h\d+")

        # Date de sortie
        item["date_sortie"] = response.css("span.release-date::text").get(default="").strip()

        yield item
