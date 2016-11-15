from setuptools import setup

setup(
    name='cloudmeta',
    version='0.0.1',
    description='Load files metadata from a cloud storage into a local DB',
    author='Carlos Henrique Romano',
    author_email='chromano@gmail.com',
    license='MIT',
    keywords='cloud storage metadata local',
    install_requires=[
        'aiobotocore==0.0.5',
        'Pillow==3.4.2',
        'motor==1.0',
    ],
    entry_points={
        'console_scripts': [
            'cloudmeta=cloudmeta.cli:main',
        ],
    }
)
