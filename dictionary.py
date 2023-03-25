import os

import pymongo
from translation_helper import TranslationHelper
from dotenv import load_dotenv




class Dictionary:
    def __init__(self):
        load_dotenv()
        self.name = ""

        self.client = pymongo.MongoClient( os.getenv('MONGO_CONNECTION_STRING'))
        # Select database
        self.db = self.client['word_learning']
        # Select collection
        self.collection = self.db['hebrew_words']
        self.translation_helper = TranslationHelper()

    def create_dictionary(self, name):
        collection = self.db[name]
        # TODO make if not already exist
        collection.insert_one({"": ""})

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_words_amount(self):
        collection = self.db[self.name]
        documents = collection.find()
        return len(list(documents))


    def insert_word(self, word):
        translate = self.translation_helper.translate_word(word)
        mydict = {"word": word, "on_hebrew": translate}
        collection = self.db[self.name]
        x = collection.insert_one(mydict)
        return x.inserted_id


    def get_all_words(self, collection_name):
        self.collection = self.db[collection_name]
        documents = self.collection.find().toArray()
        return documents

    def get_random_words(self, count):
        collection = self.db[self.name]
        #collection.aggregate([{$sample: {size: 5}}]);
