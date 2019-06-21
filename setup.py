#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='chembl_graphql',
    version='0.1.0',
    description='',
    long_description=read("README.rst"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/chembl-graphql',
    packages=['chembl_graphql', 'chembl_graphql.graph'],
    keywords="chembl graphql",
    install_requires=[
        "Flask==1.0.3",
        "graphlayer[graphql]==0.2.3",
        "sqlalchemy==1.3.4",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

