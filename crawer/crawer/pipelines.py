# -*- coding: utf-8 -*-

import pymongo

class BtPipeline(object):
    def __init__(self):
        self.Client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.DB = self.Client['bt404']
        self.Collection = self.DB['bt']

    def process_item(self, item, spider):
        try:
            self.Collection.insert_one(
                {
                    'Name': item['name'],
                    'Link': item['href'],
                    'Publish Time': item['pub_time'],
                    'File Size': item['file_size']
                }
            )
        except Exception as e:
            print('insert error:',e)

        return item
