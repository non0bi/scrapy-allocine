import pymongo
import logging

class MongoPipeline:
    collection_name = 'films'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://mongo:27017'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'allocine_db')
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.mongo_db]
            self.client.server_info()
            spider.logger.info(f"Connecté à MongoDB avec succès sur la base : {self.mongo_db}")
        except Exception as e:
            spider.logger.error(f"Impossible de se connecter à MongoDB : {e}")

    def close_spider(self, spider):
        if self.client:
            self.client.close()
            spider.logger.info("Connexion MongoDB fermée proprement.")

    def process_item(self, item, spider):
        if not item.get('url'):
            return item

        try:
            result = self.db[self.collection_name].update_one(
                {'url': item['url']},
                {'$set': dict(item)},
                upsert=True
            )
            
            if result.upserted_id:
                spider.logger.debug(f"Nouveau film inséré : {item.get('titre')}")
            else:
                spider.logger.debug(f"Film mis à jour : {item.get('titre')}")
                
        except Exception as e:
            spider.logger.error(f"Erreur lors de l'insertion du film {item.get('titre')} : {e}")
            
        return item