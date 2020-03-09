#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup


setup(
    name="nele",
    version="0.4.0",
    packages=['nele'],
    author="Raphael Zimmermann",
    author_email="dev@raphael.li",
    url="https://github.com/raphiz/nele",
    description="Send fancy newsletters with markdown",
    long_description=("For more information, please checkout the `Github Page "
                      "<https://github.com/raphiz/nele>`_."),
    license="GPL",
    platforms=["Linux"],
    include_package_data=False,
    zip_safe=False,
    install_requires=['py-gfm', 'python-frontmatter', 'jinja2', 'docopt'],
    entry_points={
        'console_scripts':
            ['nele = nele:main']
    },

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: Implementation :: CPython"
    ],
)
