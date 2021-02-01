from setuptools import setup
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyencpng',
    version='0.2a',
    description='A steganographic library to encrypt files and text in PNG images',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tadaka9/pyencpng',
    author='tadaka9',
    author_email='trapdoorfunction@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Users :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='steganography, cryptography, images',
    python_requires='>=3.6, <4',
    install_requires=['filetype', "Pillow", "pybase64", "py-cpuinfo", "pycryptodomex"],
)
