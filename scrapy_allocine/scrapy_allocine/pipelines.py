from pymongo import MongoClient

class MongoPipeline:

    def open_spider(self, spider):
        # Récupération des infos depuis settings.py
        mongo_uri = spider.settings.get("MONGO_URI", "mongodb://mongo:27017")
        mongo_db = spider.settings.get("MONGO_DATABASE", "allocine_db")
        mongo_collection = spider.settings.get("MONGO_COLLECTION", "films")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]
        self.collection = self.db[mongo_collection]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Evite les doublons sur l'URL
        self.collection.update_one(
            {"url": item["url"]},
            {"$set": dict(item)},
            upsert=True
        )
        return item
