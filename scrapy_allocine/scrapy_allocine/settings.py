BOT_NAME = "scrapy_allocine"

SPIDER_MODULES = ["scrapy_allocine.spiders"]
NEWSPIDER_MODULE = "scrapy_allocine.spiders"

# Respect du site (optionnel pour le dev)
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Pipeline MongoDB
ITEM_PIPELINES = {
    "scrapy_allocine.pipelines.MongoPipeline": 300,
}

# Encodage pour le français
FEED_EXPORT_ENCODING = "utf-8"

# Configuration MongoDB
MONGO_URI = "mongodb://mongo:27017"  # mongo = nom du container Docker
MONGO_DATABASE = "allocine_db"
MONGO_COLLECTION = "films"

# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AllocineScraper/1.0 (+https://github.com/ton-pseudo/allocine-scraper)"
