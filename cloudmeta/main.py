import asyncio
from datetime import datetime
from io import BytesIO
import time

from PIL import Image
from PIL.ExifTags import TAGS


@asyncio.coroutine
def import_metadata(db, path, filename, tags):
    """Import the given filename and tags into the given database.
    """
    tags = yield from tags
    _file = '{}/{}'.format(path, filename)
    print("[{}] IMPORTED: {}".format(datetime.now(), filename))
    yield from db.upsert(('file',), {
        'file': _file,
        'tags': tags,
    })


@asyncio.coroutine
def extract_exif(fname, contents):
    """Given the filename and its contents (a future object), tries
    to determine the file format and return its EXIF tags.

    It doesn't return any tags if the file format can't be determined
    from the given contents.
    """
    _file = yield from contents
    body = _file['Body']
    t0 = time.time()
    while True:
        try:
            content = yield from body.read()
        except asyncio.TimeoutError:
            continue
        break
    body.close()

    try:
        img = Image.open(BytesIO(content))
    except OSError:
        print("[{}] FAILED TO IMPORT (UNKNOWN FORMAT): {}".format(
            datetime.now(), fname))
        return
    tags = {}
    try:
        exif = img._getexif()
    except AttributeError:
        print("[{}] FAILED TO IMPORT (NO EXIF): {}".format(
            datetime.now(), fname))
        return
    for tag, value in exif.items():
        name = TAGS.get(tag, tag)
        tags[name] = value

    contents.close()
    return tags


@asyncio.coroutine
def run(loop, storage, db, path):
    """Given a storage, a database and a folder name, retrieves its
    files, extract file's EXIF tags and import into the db specified.
    """
    page = None
    results = []
    while True:
        result = yield from storage.listfiles(path, page)
        for _file in result['files']:
            fname = _file['filename']
            results.append(
		import_metadata(
                    db, path, fname, extract_exif(
                        fname, storage.get(path, fname))
		)
	    )
        if not 'next_page' in result:
            break
        page = result['next_page']

    if results:
        tasks = yield from asyncio.wait(results)
        return tasks
