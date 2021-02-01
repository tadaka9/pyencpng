from setuptools import setup

with open("../README.md", "r", encoding= "utf-8") as fh:
    long_description = fh.read()

setup(
    name = 'pyencpng',
    version = '0.1a',
    packages = ['pyencpng'],
    url = 'https://github.com/tadaka9/pyencpng',
    license = 'MIT',
    author = 'tadaka9',
    author_email = 'trapdoorfunction@gmail.com',
    description = 'A steganographic library to encrypt files and text in PNG images.',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
