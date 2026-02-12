BOT_NAME = "scrapy_allocine"

SPIDER_MODULES = ["scrapy_allocine.spiders"]
NEWSPIDER_MODULE = "scrapy_allocine.spiders"


ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Pipeline MongoDB
ITEM_PIPELINES = {
    "scrapy_allocine.pipelines.MongoPipeline": 300,
}

# Encodage
FEED_EXPORT_ENCODING = "utf-8"

# Configuration MongoDB
MONGO_URI = "mongodb://mongo:27017"
MONGO_DATABASE = "allocine_db"
MONGO_COLLECTION = "films"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AllocineScraper/1.0 (+https://github.com/ton-pseudo/allocine-scraper)"
