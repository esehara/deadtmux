# -*- coding: utf-8 -*-
import sys
from setuptools import setup

version = sys.version_info[:2]
install_requires = ['PyYAML', ]

if version < (2, 7) or (3, 0) <= version <= (3, 1):
    install_requires += ['argparse']

setup(
    name="deadtmux",
    description="Generate Shell Script for Tmux",
    version="0.1",
    license="MIT License",
    author="shigeo esehara",
    author_email="esehara@gmail.com",
    packages=['deadtmux', ],
    entry_points={'console_scripts': 'deadtmux=deadtmux.console:main'},
    install_requires=install_requires)
