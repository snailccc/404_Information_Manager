import pymongo

Client = pymongo.MongoClient("mongodb://localhost:27017/")
DB = Client['bt404']
Collection = DB['bt']

class BtItem:
    def __init__(self,info):
        self.name = info['name']
        self.href = info['href']
        self.pub_time = info['pub_time']
        self.file_size = info['file_size']

    @classmethod
    def InsertBt(cls, bt):
        res = Collection.insert_one(
            {
                'Name':bt.name,
                'Link':bt.href,
                'Publish Time':bt.pub_time,
                'File Size':bt.file_size
            }
        )
        return res

    @classmethod
    def Inser_Many_Bt(cls,bts):
        for it in bts:
            cls.InsertBt(it)

    @classmethod
    def Create_many_bt(cls,infos):
        return [cls(it) for it in infos]

