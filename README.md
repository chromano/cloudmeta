=========
CloudMeta
=========

A small utility for keeping track of metadata associated with images stored at a cloud storage, such as Amazon S3.

------------
Installation
------------

Checkout the repository and run the following command inside the directory created:

    pip install -e .

The `cloudmeta` command should now be available in your search path. 


-----
Usage
-----

    Usage: cloudmeta [options]

    Options:
      -h, --help            show this help message and exit
      -a AUTH, --auth=AUTH  S3 authorization key and secret separated by a colon.
                            Example: ACCESS_KEY:SECRET
      -s NAME, --s3=NAME    A S3 bucket name to import photos metadata from.
      -d NAME, --db=NAME    MongoDB collection to store pictures metadata
