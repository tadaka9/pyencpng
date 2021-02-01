"""
Author:      tadaka9
Date:        2020-25-10
Description: An encryption/decryption library for strings, hashes, files, using PNG images as container
             (generated with a cryptographically secure pseudo-random generator for RGB values),
             and an AES-256 cryptographically secure algorithm to store data.

Copyright (c) 2020 tadaka9

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
from ast import literal_eval
from cpuinfo import get_cpu_info
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from filetype import guess
from hashlib import scrypt
from io import BytesIO
from math import sqrt
from os import path, sep, urandom
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from pybase64 import urlsafe_b64encode, urlsafe_b64decode
from random import seed, shuffle, SystemRandom
from string import ascii_uppercase, ascii_lowercase, digits
from tempfile import TemporaryFile
from uuid import uuid4
from sys import maxsize


class EncPNG:
    def __init__(self, s, t, u=None):
        Image.MAX_IMAGE_PIXELS = maxsize
        self.cpuinfo = get_cpu_info()["vendor_id_raw"]
        self.data = s
        self.directory = u
        self.password = t

    @staticmethod
    def babylonian_square(i):
        """
        Check if an integer is a perfect square or not. Link -> https://en.wikipedia.org/wiki/IM_67118 .
        """
        j = i // 2
        numberslist = [j]
        while j * j != i:
            j = (j + (i // j)) // 2
            if j in numberslist:
                return False
            numberslist.append(j)
        return True

    def colors_list(self, s):
        """
        Create a list of RGB values excluding unused ones .
        """
        dataset = self.unique_pair()
        colorslist = []
        fixedly = int(len(s) - 1)
        for i, j in enumerate(s):
            colorslist.append(dataset[s[i]])
        size = self.square_size()
        for i in range(size - fixedly):
            randtuple = self.rand(), self.rand(), self.rand()
            while randtuple in dataset.values():
                randtuple = self.rand(), self.rand(), self.rand()
            colorslist.append(randtuple)
        return colorslist, dataset

    def decrypt(self, s=None):
        """
        Decrypt image data using stored as ztEXt chunks and reverting RGB values to
        dataset; store decrypted data to a file or return as bytes
        """
        if not self.directory:
            img = Image.open(s)
            metadata = img.info
        else:
            img = Image.open(self.data)
            assert isinstance(img.info, dict)
            metadata = img.info

        datasetdict = dict(CipherData = metadata["Dataset"],
                           Nonce = metadata["DatasetNonce"],
                           Salt = metadata["DatasetSalt"],
                           Tag = metadata["DatasetTag"])
        colorslist = list(img.getdata())
        dataset = literal_eval(bytes.decode(self.decrypt_aes256(datasetdict)))
        with TemporaryFile(mode='w+b') as f:
            for letter in self.mapem(colorslist, dataset):
                f.write(bytes(letter, "utf-8"))
            f.seek(0)
            data = f.read()
            f.close()
        datadict = dict(CipherData = data,
                        Nonce = metadata["DataNonce"],
                        Salt = metadata["DataSalt"],
                        Tag = metadata["DataTag"])
        data = urlsafe_b64decode(self.decrypt_aes256(datadict))
        if self.directory:
            if guess(data) is None:
                with open(self.directory + sep + path.splitext(path.basename(self.data))[0] + ".txt", "wb") as f:
                    f.write(data)
                    f.close()
            else:
                with open(self.directory + sep + path.splitext(path.basename(self.data))[0] + "."
                          + guess(data).extension, "wb") as f:
                    f.write(data)
                    f.close()
        else:
            return data.decode('utf-8')

    def decrypt_aes256(self, dictionary):
        """"
        Decrypt a dictionary of AES-256 items, returning a base64 string
        """
        cipherdata = urlsafe_b64decode(dictionary["CipherData"])
        nonce = urlsafe_b64decode(dictionary["Nonce"])
        salt = urlsafe_b64decode(dictionary["Salt"])
        tag = urlsafe_b64decode(dictionary["Tag"])
        privatekey = scrypt(self.password.encode(), salt = salt, n = 2 ** 14, r = 8, p = 1, dklen = 32)
        if "Intel" in self.cpuinfo:
            cipher = AES.new(privatekey, AES.MODE_GCM, nonce = nonce, use_aesni = True)
        else:
            cipher = AES.new(privatekey, AES.MODE_GCM, nonce = nonce)
        decrypted = cipher.decrypt_and_verify(cipherdata, tag)
        return decrypted

    def encrypt(self):
        """
        Encode in base64 the string/file, create a PNG file with previously selected
        colors; encrypt in AES-256 characters + RGB values dataset, and append to
        image as zTXt chunk; save PNG file with uuid4 filename or return image PIL object
        depending on directory parameter.
        """
        if path.isfile(self.data):
            with open(self.data, "rb") as file:
                self.data = urlsafe_b64encode(file.read()).decode('utf8')
            file.close()
        else:
            self.data = urlsafe_b64encode(self.data.encode()).decode('utf8')
        encrypted = self.encrypt_aes256(dataset=None)
        self.data = encrypted["CipherData"]
        colorslist, dataset = self.colors_list(self.data)
        imgsize = int(sqrt(len(colorslist)))
        img = Image.new(mode = "RGB", size = (imgsize, imgsize))
        img.putdata(colorslist)
        encdataset = self.encrypt_aes256(str(dataset))
        metadata = PngInfo()
        metadata.add_text("Dataset", encdataset["CipherData"], zip = True)
        metadata.add_text("DatasetNonce", encdataset["Nonce"], zip = True)
        metadata.add_text("DatasetSalt", encdataset["Salt"], zip = True)
        metadata.add_text("DatasetTag", encdataset["Tag"], zip = True)
        metadata.add_text("DataNonce", encrypted["Nonce"], zip = True)
        metadata.add_text("DataSalt", encrypted["Salt"], zip = True)
        metadata.add_text("DataTag", encrypted["Tag"], zip = True)
        if not self.directory:
            b = BytesIO()
            img.save(b, "PNG", pnginfo = metadata)
            b.seek(0)
            return b
        img.save(self.directory + sep + str(uuid4()) + ".png", "PNG", pnginfo = metadata)

    def encrypt_aes256(self, dataset):
        """
        Encrypt a string in aes256, returning a dictionary with ciphered text, salt, nonce, tag.
        """
        salt = get_random_bytes(AES.block_size)
        privatekey = scrypt(self.password.encode(), salt = salt, n = 2 ** 14, r = 8, p = 1, dklen = 32)
        if "Intel" in self.cpuinfo:
            config = AES.new(privatekey, AES.MODE_GCM, use_aesni = True)
        else:
            config = AES.new(privatekey, AES.MODE_GCM)
        if dataset:
            cipherdata, tag = config.encrypt_and_digest(bytes(dataset, 'utf-8'))
        else:
            cipherdata, tag = config.encrypt_and_digest(bytes(self.data, 'utf-8'))
        return {
            "CipherData": urlsafe_b64encode(cipherdata).decode('utf-8'),
            "Nonce": urlsafe_b64encode(config.nonce).decode('utf-8'),
            "Salt": urlsafe_b64encode(salt).decode('utf-8'),
            "Tag": urlsafe_b64encode(tag).decode('utf-8')
        }

    def mapem(self, iterable, mapping):
        dd = {v: k for k, v in mapping.items()}
        for t in iterable:
            mapped = dd.get(t)
            if mapped:
                yield mapped

    @staticmethod
    def rand():
        return SystemRandom().randint(0, 255)

    def square_size(self):
        """
        Make length of string a perfect square.
        """
        s = len(self.data) - 1
        while not self.babylonian_square(s):
            s += 1
        return s - 1

    def unique_pair(self):
        """
        Create an unique pairing between character type and tuple type; create an unique namefile.
        """
        charset = list(ascii_uppercase + ascii_lowercase + digits) + ["+", "/", "=", "-", "_"]
        dataset = {}
        seed(urandom(20000000))
        shuffle(charset)
        for i in charset:
            randtuple = self.rand(), self.rand(), self.rand()
            while randtuple in dataset.values():
                randtuple = self.rand(), self.rand(), self.rand()
            dataset[i] = randtuple
        return dataset
