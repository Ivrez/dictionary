import ssl

from pymongo import MongoClient

from bson.objectid import ObjectId

from conf.conf import mongo_user 
from conf.conf import mongo_passwd
from conf.conf import mongo_hostname

class DefaultMongoDB():
    def __init__(self):
        user = mongo_user
        passwd = mongo_passwd
        hostname = mongo_hostname
        conn = 'mongodb+srv://' + user + ':' + passwd + '@' + hostname

        client = MongoClient(conn)
        #client = MongoClient(conn, ssl_cert_reqs=ssl.CERT_NONE)

        self.db = client.englearn

    def add_words(self, word_eng, word_rus, word_cn):
        data = {
                'word_eng': word_eng,
                'word_rus': word_rus,
                'word_cn': word_cn,
        }
        self.db.words.insert(data)
        return

    def get_full_dict(self):
        data = self.db.words.find({})
        return data

    def get_random_word(self, count):
        data = self.db.words.aggregate([{'$sample': {'size': count}}])
        return data

    def update_words(self, word_id, word_eng, word_rus, word_cn):
        data = {
                '$set': {}
                }

        if word_eng is not None:
            data['$set']['word_eng'] = word_eng
        if word_rus is not None:
            data['$set']['word_rus'] = word_rus
        if word_cn is not None:
            data['$set']['word_cn'] = word_cn

        self.db.words.update_one({'_id': ObjectId(word_id)}, data, upsert=False)
        return

    def get_words(self, word_id):
        data = self.db.words.find_one({'_id': ObjectId(word_id)})
        return data

    def delete_words(self, word_id):
        data = self.db.words.delete_one({'_id': ObjectId(word_id)})
        return data
