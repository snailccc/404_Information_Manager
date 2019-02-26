# -*- coding= utf-8 -*-
import codecs
import sys
import pymongo

reload(sys)
sys.setdefaultencoding('utf8')

Client = pymongo.MongoClient('mongodb://localhost:27017/')
DB= Client['bt404']
Collection = DB['bt']
