"""
Author:      tadaka9
Date:        2020-25-10
Description: An encryption/decryption commandline-library for strings, hashes, files, using PNG images as container
             (generated with a cryptographically secure random generator for RGB values),
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
from argparse import ArgumentParser
from encpng import EncPNG
from multiprocessing import freeze_support
from sys import exit, stderr


class Parser(ArgumentParser):
    def error(self, message):
        stderr.write("Error: %s\n" % message)
        self.print_help()
        exit(2)

if __name__ == '__main__':
    freeze_support()
    parser = Parser(add_help=True, allow_abbrev=True, description="A steganographic encryption/decryption tool")
    parser.add_argument("-d", "--decrypt", nargs = "+", metavar = "FILE", help = "Usage: [-d | --decrypt] FILE")
    parser.add_argument("-dir", "--directory", metavar = 'PATH', nargs = "+",
        help = "Usage: [-dir or --directory] PATH", required=False)
    parser.add_argument("-e", "--encrypt", nargs = "+", metavar = ("FILE or STRING", "FILE or STRING"),
        help = "Usage: [-e or --encrypt] FILE or STRING")
    parser.add_argument("-p", "--password", metavar = 'STRING',
        nargs = "+", help = "Usage: [-p or --password] STRING")
    args = parser.parse_args()
    if not args.decrypt and not args.encrypt and not args.directory:
        parser.error("Error: arguments not specified")
    if args.decrypt:
        EncPNG(" ".join(args.decrypt), " ".join(args.password), " ".join(args.directory)).decrypt()
    if args.encrypt:
        EncPNG(" ".join(args.encrypt), " ".join(args.password), " ".join(args.directory)).encrypt()
