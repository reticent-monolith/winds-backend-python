import pymongo
import datetime
import enum
import pprint
import bson


class Slider(enum.Enum):
    BLACK = 1
    OLD_RED = 2
    NEW_RED = 3
    YELLOW = 4

    def __str__(self):
        return self.name


class Rider:
    def __init__(self, weight, trolley, front=None, middle=None, rear=None, added=0, speed=0):
        self.weight = weight
        self.trolley = trolley
        self.frontSlider = front
        self.middleSlider = middle
        self.rearSlider = rear
        self.addedWeight = added
        self.speed = speed

    @classmethod
    def from_dict(cls, d):
        return cls(
            weight=d['weight'],
            trolley=d['trolley'],
            front=d['frontSlider'] if 'frontSlider' in d.keys() else None,
            middle=d['middleSlider'] if 'middleSlider' in d.keys() else None,
            rear=d['rearSlider'] if 'rearSlider' in d.keys() else None,
            added=d['addedWeight'] if 'addedWeight' in d.keys() else None,
            speed=d['speed'] if 'speed' in d.keys() else None
        )


class Dispatch:
    def __init__(self, wind_deg, wind_spd, bt, inst, date, time, comment="", riders={'1': None, '2': None, '3': None, '4': None}, _id=None):
        self.riders = riders
        self.date = date
        self.time = time
        self._id = _id if _id else None
        self.wind_degrees = wind_deg
        self.wind_speed = wind_spd
        self.bt_radio = bt
        self.winds_instructor = inst
        self.comment = comment

    def __repr__(self):
        return pprint.pformat(self.as_dict())

    def as_dict(self):
        return {
            'riders': {line: rider.__dict__ for line, rider in self.riders.items()},
            'windDegrees': self.wind_degrees,
            'windSpeed': self.wind_speed,
            'date': self.date,
            'time': self.time,
            'btRadio': self.bt_radio,
            'windsInstructor': self.winds_instructor,
            'comment': self.comment,
            '_id': str(self._id) 
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            wind_deg=d['windDegrees'],
            wind_spd=d['windSpeed'],
            bt=d['btRadio'],
            inst=d['windsInstructor'],
            date=d['date'],
            time=d['time'],
            comment=d['comment'],
            riders={line: Rider.from_dict(rider)
                    for line, rider in d['riders'].items()},
            _id=bson.ObjectId(d['_id']) if '_id' in d.keys() else bson.ObjectId()
        )


class DispatchRepo:
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
