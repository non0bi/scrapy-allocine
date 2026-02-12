import scrapy
import re

class AllocineFilmsSpider(scrapy.Spider):
    name = "allocine_films"
    allowed_domains = ["allocine.fr"]
    
    def start_requests(self):
        base_url = "https://www.allocine.fr/film/aucinema/?page="
        for i in range(1, 11):
            yield scrapy.Request(url=f"{base_url}{i}", callback=self.parse)

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_allocine.pipelines.MongoPipeline': 300,
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 1.5, # Un peu plus rapide car on multiplie les requêtes
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
    }

    def parse(self, response):
        films = response.css("div.card.entity-card-list")
        for film in films:
            item = {}
            titre_node = film.css("a.meta-title-link")
            item["titre"] = titre_node.css("::text").get("").strip()
            
            if not item["titre"]:
                continue

            url_path = titre_node.css("::attr(href)").get()
            if url_path:
                item["url"] = response.urljoin(url_path)
                # On récupère la note ici car elle est plus facile à trouver sur la liste
                item["note_spectateurs"] = film.css(".stareval-note::text").get()

                # On suit le lien vers la page de détails pour TOUT le reste (image incluse)
                yield response.follow(
                    item["url"],
                    callback=self.parse_film,
                    meta={"item": item}
                )

    def parse_film(self, response):
        item = response.meta["item"]
        
        # --- EXTRACTION DE L'AFFICHE (VERSION ROBUSTE) ---
        # Sur la fiche film, l'image principale est dans l'entité 'figure.thumbnail'
        img_url = response.css("figure.thumbnail img::attr(src)").get()
        
        # Sécurité : si Allociné utilise encore un placeholder sur la fiche
        if not img_url or "empty.gif" in img_url:
            img_url = response.css("figure.thumbnail img::attr(data-src)").get()
            
        item["affiche_url"] = img_url

        # Synopsis
        synopsis_nodes = response.css("div#synopsis-details div.content-txt::text").getall()
        if not synopsis_nodes:
             synopsis_nodes = response.css("section.synopsis-section div.content-txt::text").getall()
        item["synopsis"] = " ".join([t.strip() for t in synopsis_nodes if t.strip()])

        # Genre et autres infos
        genres = response.css("div.meta-body-info span.dark-grey-link::text").getall()
        item["genre"] = [g.strip() for g in genres if g.strip()]

        # Extraction de la durée via texte brut
        info_text = response.css("div.meta-body-info::text").getall()
        info_string = " ".join(info_text)
        duration_match = re.search(r"(\d+h\s*\d*m?i?n?)", info_string)
        item["duree"] = duration_match.group(1).strip() if duration_match else "N/A"

        # Date de sortie
        date_node = response.css("span.date::text").get()
        item["date_sortie"] = date_node.strip() if date_node else "Inconnue"

        yield item