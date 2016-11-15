"""This is the code for the Command Line Interface.
"""
import asyncio
from optparse import OptionParser

from cloudmeta.dbs.mongo import MongoDB
from cloudmeta.main import run
from cloudmeta.storages.s3 import ReadOnlyS3


def main():
    """Retrieves parameters specified from command line and start the
    importing process accordingly.
    """
    parser = OptionParser()

    parser.add_option("-a", "--auth", dest="auth",
        metavar='AUTH',
        help=('S3 authorization key and secret separated by a colon. '
              'Example: ACCESS_KEY:SECRET'))
    parser.add_option("-s", "--s3", dest="s3",
        metavar='NAME',
        help='A S3 bucket name to import photos metadata from.')
    parser.add_option("-d", "--db", dest="db",
        metavar='NAME',
        help="MongoDB collection to store pictures metadata")

    (options, args) = parser.parse_args()
    if not all((options.auth, options.s3, options.db)):
        parser.print_help()
        return

    valid = True
    parts = options.auth.split(':')
    if len(parts) != 2:
        valid = False
    else:
        key, secret = parts

    if not valid:
        parser.print_help()
    else:
        loop = asyncio.get_event_loop()

        storage = ReadOnlyS3()
        storage.connect(loop, key=key, secret=secret)

        db = MongoDB()
        db.connect(
            'mongodb://localhost:27017/cloudmeta/{}'.format(options.db))

        loop.run_until_complete(
            run(loop, storage, db, options.s3))

        storage.disconnect()
        loop.stop()
