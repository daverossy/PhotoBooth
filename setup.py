from setuptools import setup

setup(
    name='PhotoBooth',
    version='1.0',
    packages=[''],
    install_requires=[
        'picamera',
        'pygame',
        'pycups',
        'RPi.GPIO',
        'time',
        'os',
        'datetime',
    ],
    url='http://github.com/daverossy/PhotoBooth',
    license='MIT',
    author='Dave Rossiter',
    author_email='',
    description='',
    include_package_data=True,
    zip_safe=False)
