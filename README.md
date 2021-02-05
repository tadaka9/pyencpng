# PyEncPNG

<img src="https://travis-ci.com/tadaka9/pyencpng.svg?branch=master"></a>

A steganographic commandline to library, to encrypt files and text in PNG images using CSPRNG random generated pixel colors, shuffled charset for pybase64, and AES-256 with tag (anti-tamper support, and with Intel-NI support on Intel processors) to encrypt or decrypt data (full UTF-8 support).

## BLOCKCHAIN INFOS:

This is the base library to build the Laniakea ([Laniakea Supercluster](https://en.wikipedia.org/wiki/Laniakea_Supercluster)) blockchain (to be developed).

## INSTALLATION

Use the package manager [pip](https://pip.pypa.io/en/stable/) and [git](https://git-scm.com/) distributed version control to install EncPNG.
<br>On Linux, MacOS, and Windows's Cygwin (or MinGW), GCC or Clang should be installed.</br>
<br>On Windows, Microsoft C/C++ compiler (for Visual Studio) should be installed (to avoid errors like: "Unable to find vcvarsall.bat").</br>
OpenSSL should be installed.
<br>If you get memory error from Python, increase Windows paging or Linux swap.<br>
## Installation instructions

```bash
# Make sure you have the latest versions of pip, setuptools and wheel installed
python3 -m pip install --upgrade pip setuptools wheel
pip3 install encpng
git clone https://github.com/tadaka9/pyencpng.git
cd pyencpng
```
## USAGE
```
python3 encpng-cli.py [ [ -dir or --directory ] OUTPUT_PATH [ -e or --encrypt ] STRING or FILE [ -p or --password ] PASSWORD ] or [ [ --dir or --directory ] OUTPUT_PATH [ -d or --decrypt ] FILE [ -p or --password ] PASSWORD ]
```
## EXAMPLES
```python
python3 encpng-cli.py --dir out/dir/path --encrypt file.txt --password Password1 23!"£
```
```python
python encpng-cli.py --dir out/dir/path --decrypt 08a30930-ecdf-4f6a-9978-c274093d63e1.png --password Password1 23!"£
```
