"""This file specifies interfaces needed by cloudmeta in order to interact
with cloud storages.

These are abstract classes from a technical POV, you are not supposed to
instantiate them directly.
"""


class AbstractReadOnlyStorage(object):
    """Interface for read-only access to a cloud storage.
    """
    def connect(self, loop, **kwargs):
        """Establishes a connection to the cloud provider, keeping the
        session stored locally in order to avoid multiple connections
        when performing multiple actions.
        
        The arguments vary depending on the provider, but the first
        parameter `loop` is always required and corresponds to the
        eventloop in use for async operations.
        """
        raise NotImplementedError()

    def disconnect(self):
        """Closes active connection to the cloud provider, required
        after you are done.
        """

    def listfiles(self, path):
        """Given a path (also called a bucket on some cloud providers),
        yield a list of dictionaries containing information about each
        file found. It is guaranteed the following attributes on the
        dictionaries:

            - `filename`: the filename, can be used with the `.get`
              method in order to retrieve the file content;
            - `size`: the file size.

        The results will be in the following format:

            {'files': [...list of dicts...], 'next_page': 'ABC123'}

        If `next_page` is available in the results, this method can be
        called again with that value in order to retrieve the next
        page of files.
        """
        raise NotImplementedError()

    def get(self, _id):
        """Given a file ID (as returned by `listfiles`), yield the file
        content.
        """
        raise NotImplementedError()
