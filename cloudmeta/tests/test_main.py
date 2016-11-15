import asyncio

import asynctest

from cloudmeta.main import run


class TestRun(asynctest.TestCase):
    @asynctest.mock.patch('cloudmeta.main.import_metadata')
    def test_empty_storage(self, import_metadata):
        """Ensure nothing is imported if the storage has no files.
        """
        storage = asynctest.CoroutineMock()
        storage.listfiles.return_value = {'files': []}
        db = asynctest.MagicMock()
        results = yield from run(self.loop, storage, db, 'test')

        self.assertIsNone(results)

        import_metadata.assert_not_called()

    @asynctest.mock.patch('cloudmeta.main.extract_exif')
    @asynctest.mock.patch('cloudmeta.main.import_metadata')
    def test_multiple_pages(self, import_metadata, extract_exif):
        """Ensure storage results with multiple pages are processed
        correctly.
        """
        storage = asynctest.CoroutineMock()
        storage.listfiles.side_effect = [{
            'files': [
                {'filename': 'foo.txt'},
            ],
            'next_page': '2'
        }, {
            'files': [
                {'filename': 'bar.txt'},
            ],
        }]
        db = asynctest.MagicMock()
        results = yield from run(self.loop, storage, db, 'test')

        import_metadata.assert_any_call(
            db, 'test', 'bar.txt', asynctest.mock.ANY)
        import_metadata.assert_any_call(
            db, 'test', 'foo.txt', asynctest.mock.ANY)

    @asynctest.mock.patch('cloudmeta.main.extract_exif')
    def test_extract_exif_exception(self, extract_exif):
        """Ensure an exception on EXIF tags extraction won't affect
        other files being processed.
        """
        storage = asynctest.CoroutineMock()
        storage.listfiles.side_effect = [{
            'files': [
                {'filename': 'foo.txt'},
            ],
            'next_page': '2'
        }, {
            'files': [
                {'filename': 'bar.txt'},
            ],
        }]
        extract_exif.side_effect = asynctest.return_once(
            iter(['a', 'b', 'c']), TypeError("This is a test"))
        db = asynctest.MagicMock()
        results = yield from run(self.loop, storage, db, 'test')

        db.upsert.assert_called_once_with(
            asynctest.mock.ANY, asynctest.mock.ANY)

    @asynctest.mock.patch('cloudmeta.main.import_metadata')
    def test_import_metadata_exception(self, import_metadata):
        """Ensure an exception on importing process won't affect
        other files being processed.
        """
        storage = asynctest.CoroutineMock()
        storage.listfiles.side_effect = [{
            'files': [
                {'filename': 'foo.txt'},
            ],
            'next_page': '2'
        }, {
            'files': [
                {'filename': 'bar.txt'},
            ],
        }]
        import_metadata.side_effect = asynctest.return_once(
            0, TypeError("This is a test"))
        db = asynctest.MagicMock()
        result = yield from run(self.loop, storage, db, 'test')
        done, cancelled = result

        self.assertEqual(len(done), 2)

        exceptions = [d.exception() for d in done if d.exception()]

        self.assertEqual(len(exceptions), 1)

    @asynctest.mock.patch('cloudmeta.main.extract_exif')
    def test_ensure_tasks(self, extract_exif):
        """Ensure tasks complete properly if there are no exceptions
        involved.
        """
        storage = asynctest.CoroutineMock()
        storage.listfiles.side_effect = [{
            'files': [
                {'filename': 'foo.txt'},
            ],
            'next_page': '2'
        }, {
            'files': [
                {'filename': 'bar.txt'},
            ],
        }]
        extract_exif.side_effect = [
            iter(['a', 'b', 'c']), iter(['a', 'b', 'c'])
        ]

        db = asynctest.MagicMock()
        results = yield from run(self.loop, storage, db, 'test')

        db.upsert.assert_any_call(
            asynctest.mock.ANY,
            {'file': 'test/foo.txt', 'tags': asynctest.mock.ANY})
        db.upsert.assert_any_call(
            asynctest.mock.ANY,
            {'file': 'test/bar.txt', 'tags': asynctest.mock.ANY})
