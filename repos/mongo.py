import pymongo
from models.dispatch import Dispatch


class MongoDispatchRepo:
    def __init__(self, conn_str):
        self._conn = pymongo.MongoClient(
            conn_str, serverSelectionTimeoutMS=5000)
        self._db = self._conn.zw
        self._collection = self._db.winds

    def get_all(self) -> list:
        from_db = list(self._collection.find())
        return [Dispatch.from_dict(x) for x in from_db]

    def by_id(self, _id) -> Dispatch:
        return Dispatch.from_dict(self._collection.find_one({'_id': _id}))

    def by_date(self, date: str) -> Dispatch:
        from_db = list(self._collection.find({'date': date}))
        return [Dispatch.from_dict(x) for x in from_db]

    def delete(self, dispatch: Dispatch):
        self._collection.delete_one({'_id': dispatch._id})

    def update(self, dispatch: Dispatch):
        self._collection.update_one({'_id': dispatch._id}, dispatch)

    def add(self, dispatch: Dispatch) -> int:
        self._collection.insert_one(dispatch.as_dict())
