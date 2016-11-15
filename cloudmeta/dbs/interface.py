"""This file specifies interfaces needed by cloudmeta in order to interact
with databases.

These are abstract classes from a technical POV, you are not supposed to
instantiate them directly.
"""


class AbstractDB(object):
    """Interface for operations on databases
    """
    def connect(self, dsn):
        """Given the database DNS, establish a new connection. This is
        required before any other method is called.
        """

    def upsert(self, unique, record):
        """Given a dictionary representing a database record, insert or
        update the record depending on the `unique` parameters given.

        Example: 

            upsert(('filename',), {
                'filename': 'test.txt',
                'datemod': '20161110T13:45:00Z0000',
            })

        In the example above, if there's a record with `filename` equals
        to `test.txt`, then this method will issue an update operation,
        otherwise it will insert a new record in the database.
        """
        raise NotImplementedError()
