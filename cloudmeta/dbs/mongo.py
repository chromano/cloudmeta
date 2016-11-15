import motor.motor_asyncio

from cloudmeta.dbs.interface import AbstractDB


class MongoDB(AbstractDB):
    def __init__(self):
        self.client = None
        self.db = None
        self.coll = None

    def connect(self, dsn):
        dsn, db, coll = dsn.rsplit('/', 2)
        self.client = motor.motor_asyncio.AsyncIOMotorClient()
        self.db = self.client[db]
        self.coll = self.db[coll]

    def upsert(self, unique, record):
        uniques = {}
        for attr in unique:
            uniques[attr] = record[attr]

        # A normalization of keys is necessary, since MongoDB won't allow
        # records with keys in a data type other than strings.
        def _normalize_keys(d):
            for key in d.keys():
                value = d[key]
                if not isinstance(key, str):
                    d[str(key)] = d.pop(key)
                if isinstance(value, dict):
                    _normalize_keys(value)
        _normalize_keys(record)

        yield from self.coll.update_one(
                uniques, {'$set': record}, upsert=True)
