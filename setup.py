# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="deadtmux",
    description="Generate Shell Script for Tmux",
    version="0.1",
    license="MIT License",
    author="shigeo esehara",
    author_email="esehara@gmail.com",
    packages=['deadtmux', ],
    entry_points={'console_scripts': 'deadtmux=deadtmux:commands'},
    install_requires=['PyYAML', ])
