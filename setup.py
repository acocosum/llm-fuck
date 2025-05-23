#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llm-fuck",
    version="0.1.0",
    author="hongyu1128",
    author_email="your.email@example.com",
    description="使用大语言模型修正命令行错误的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/llm-fuck",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "pyyaml>=5.4.0",
    ],
    entry_points={
        "console_scripts": [
            "llmf=llm_fuck.main:main",
        ],
    },
)