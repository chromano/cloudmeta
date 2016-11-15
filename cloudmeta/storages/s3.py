import asyncio

import aiobotocore

from cloudmeta.storages.interface import AbstractReadOnlyStorage


class ReadOnlyS3(AbstractReadOnlyStorage):
    def __init__(self):
        self._session = None
        self._client = None

    def connect(self, loop, key, secret):
        self._session = aiobotocore.get_session(loop=loop)
        self._client = self._session.create_client(
            's3', region_name='us-west-2', aws_secret_access_key=secret,
            aws_access_key_id=key)

    def disconnect(self):
        self._client.close()

    @asyncio.coroutine
    def listfiles(self, path, page=None):
        kwargs = {'Bucket': path, 'MaxKeys': 1000}
        if page is not None:
            kwargs['Marker'] = page
        contents = yield from self._client.list_objects(**kwargs)
        result = {'files': []}
        if contents['IsTruncated']:
            result['next_page'] = contents.get(
                'NextMarker', contents['Contents'][-1]['Key'])
        for entry in contents['Contents']:
            result['files'].append({
                'filename': entry['Key'],
                'size': entry['Size']
            })
        return result

    @asyncio.coroutine
    def get(self, path, _id):
        return self._client.get_object(Bucket=path, Key=_id)
