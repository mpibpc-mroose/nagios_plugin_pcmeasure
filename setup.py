import sys
import os
from setuptools import setup

version = '0.1.0'

setup(
    name='nagios_plugin_pcmeasure',
    version=version,
    author='Dr. Marco Roose',
    author_email='marco.roose@mpibpc.mpg.de',
    url='https://github.com/mpibpc-mroose/nagios_plugin_pcmeasure/',
    license='GPL-3.0',
    description='Nagios Plugin for ethernet sensor boxes from http://messpc.de',
    long_description='Please see our GitHub README',
    install_requires=[],
    keywords=[
        'Nagios',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
