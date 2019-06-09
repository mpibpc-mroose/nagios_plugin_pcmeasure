#!/usr/bin/env python3

from setuptools import setup

version = '0.1.0'

setup(
    name='check__pcmeasure',
    version=version,
    author='Dr. Marco Roose',
    author_email='marco.roose@mpibpc.mpg.de',
    url='https://github.com/mpibpc-mroose/nagios_plugin_pcmeasure/',
    license='GPL-3.0',
    description='Nagios/Icinga Plugin for ethernet sensor boxes from http://messpc.de',
    long_description='Please see our GitHub README',
    install_requires=[],
    keywords=[
        'Nagios',
        'Icinga'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        'Programming Language :: Python :: 3.7'
    ]
)
