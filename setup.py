#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup


setup(
    name="nele",
    version="0.1.0",
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
    install_requires=open('./requirements.txt').read(),
    entry_points={
        'console_scripts':
            ['nele = nele:main']
    },

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: Implementation :: CPython",
        'Development Status :: 4 - Beta',
    ],
)
