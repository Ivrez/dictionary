import sys

from db.db import DefaultDB
from db_mongo.db import DefaultMongoDB

class Functions():
    def __init__(self, local=None):
        if local is not None:
            self.db = DefaultDB()
        self.db = DefaultMongoDB()

    def get_words(self, id):
        try:
            return self.db.get_words(id)
        except Exception as err:
            return str(err)

    def add_words(self, eng=None, rus=None, cn=None):
        try:
            self.db.add_words(eng, rus, cn)
        except Exception as err:
            return str(err)

    def update_words(self, id, eng=None, rus=None, cn=None):
        try:
            return self.db.update_words(id, eng, rus, cn)
        except Exception as err:
            return str(err)

    def delete_words(self, id):
        try:
            return self.db.delete_words(id)
        except Exception as err:
            return str(err)

    def get_full_dict(self):
        try:
            return self.db.get_full_dict()
        except Exception as err:
            return str(err)

    def get_random_word(self, count=1):
        try:
            return self.db.get_random_word(count)
        except Exception as err:
            return str(err)
