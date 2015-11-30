# -*- coding: utf-8 -*-
"""Installer for the collective.behavior.banner package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('CHANGELOG.rst') + \
    read('docs/source', 'LICENSE.rst')

setup(
    name='collective.behavior.banner',
    version='1.0a1',
    description="A behavior to create sliders with banners",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
    ],
    keywords='Python, Plone, Dexterity, behavior',
    author='Philip Bauer',
    author_email='bauer@starzel.de',
    url='http://pypi.python.org/pypi/collective.behavior.banner',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.behavior'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone',
        'setuptools',
        'plone.api',
    ],
    extras_require={
        'test': [
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'plone.app.testing',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
