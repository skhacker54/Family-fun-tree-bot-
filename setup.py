"""
Setup script for Fam Tree Bot
==============================
Installation and setup helper
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fam-tree-bot",
    version="2.0.0",
    author="Fam Tree Bot Team",
    author_email="support@famtreebot.com",
    description="The Ultimate Telegram Family Simulation RPG Bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fam-tree-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fam-tree-bot=bot:main",
        ],
    },
)
