#!/usr/bin/env python3

import setuptools


version = '0.2.0'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='check__pcmeasure.py',
    version=version,
    author='Dr. Marco Roose',
    author_email='marco.roose@mpibpc.mpg.de',
    url='https://github.com/mpibpc-mroose/nagios_plugin_pcmeasure/',
    license='GPL-3.0',
    description='Nagios/Icinga2 Plugin for ethernet sensor boxes from http://messpc.de and http://pcmeasure.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    python_requires='>=3.5',
    packages=setuptools.find_packages(),
    project_urls={
        'Source': 'https://github.com/mpibpc-mroose/nagios_plugin_pcmeasure/',
        'Nagios Exchange': 'https://exchange.nagios.org/',
        'Icinga Exchange': 'https://exchange.icinga.com',
     },
    keywords=[
        'Nagios',
        'Icinga2',
        'pcmeasure',
        'messpc',
        'etherbox'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
