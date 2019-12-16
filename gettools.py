#!/usr/bin/env python
"""
The MIT License (MIT)

Copyright (c) 2015-2017 Dave Parsons

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from __future__ import print_function
import os
import sys
import shutil
import tarfile
import zipfile
import time

try:
    # For Python 3.0 and later
    # noinspection PyCompatibility
    from urllib.request import urlopen
    # noinspection PyCompatibility
    from html.parser import HTMLParser
    # noinspection PyCompatibility
    from urllib.request import urlretrieve
except ImportError:
    # Fall back to Python 2
    # noinspection PyCompatibility
    from urllib2 import urlopen
    # noinspection PyCompatibility
    from HTMLParser import HTMLParser
    # noinspection PyCompatibility
    from urllib import urlretrieve


# Parse the Fusion directory page
class CDSParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.HTMLDATA = []

    def handle_data(self, data):
        # Build a list of numeric data from any element
        if data.find("\n") == -1:
            if data[0].isdigit():
                self.HTMLDATA.append(data)
                self.HTMLDATA.sort(key=lambda s: [int(u) for u in s.split('.')])

    def clean(self):
        self.HTMLDATA = []


def convertpath(path):
    # OS path separator replacement funciton
    return path.replace(os.path.sep, '/')


def main():
    # Check minimal Python version is 2.7
    if sys.version_info < (2, 7):
        sys.stderr.write('You need Python 2.7 or later\n')
        sys.exit(1)

    dest = os.path.dirname(os.path.abspath(__file__))

    # Re-create the tools folder
    shutil.rmtree(dest + '/tools', True)
    os.mkdir(dest + '/tools')

    parser = CDSParser()
    success = False
    n = 1

    # Last published version doesn't ship with darwin tools
    # so in case of error fall back to the latest version that has them
    while (success == False):
        print('Trying for the '+str(n)+'th time')

        # Setup url and file paths
        url = 'http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/'

        # Get the list of Fusion releases
        # And get the last item in the ul/li tags
        
        response = urlopen(url)
        html = response.read()
        parser.clean()
        parser.feed(str(html))
        url = url + parser.HTMLDATA[-n] + '/'
        parser.clean()

        # Open the latest release page
        # And build file URL
        response = urlopen(url)
        html = response.read()
        parser.feed(str(html))
        
        urlpost15 = url + parser.HTMLDATA[-1] + '/packages/com.vmware.fusion.tools.darwin.zip.tar'
        urlpre15 = url + parser.HTMLDATA[-1] + '/packages/com.vmware.fusion.tools.darwinPre15.zip.tar'
        parser.clean()

        # Download the darwin.iso tgz file
        print('Retrieving Darwin tools from: ' + urlpost15)
        try:
            urlretrieve(urlpost15, convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip.tar'))

        except:
            print('Link didn\'t work, trying another one...')
            n += 1
            continue

        # Extract the tar to zip
        tar = tarfile.open(convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip.tar'), 'r')
        tar.extract('com.vmware.fusion.tools.darwin.zip', path=convertpath(dest + '/tools/'))
        tar.close()

        # Extract the iso and sig files from zip
        cdszip = zipfile.ZipFile(convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip'), 'r')
        cdszip.extract('payload/darwin.iso', path=convertpath(dest + '/tools/'))
        cdszip.extract('payload/darwin.iso.sig', path=convertpath(dest + '/tools/'))
        cdszip.close()

        # Move the iso and sig files to tools folder
        shutil.move(convertpath(dest + '/tools/payload/darwin.iso'), convertpath(dest + '/tools/darwin.iso'))
        shutil.move(convertpath(dest + '/tools/payload/darwin.iso.sig'), convertpath(dest + '/tools/darwin.iso.sig'))

        # Cleanup working files and folders
        shutil.rmtree(convertpath(dest + '/tools/payload'), True)
        os.remove(convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip.tar'))
        os.remove(convertpath(dest + '/tools/com.vmware.fusion.tools.darwin.zip'))

        # Download the darwinPre15.iso tgz file
        print('Retrieving DarwinPre15 tools from: ' + urlpre15)
        try:
            urlretrieve(urlpre15, convertpath(dest + '/tools/com.vmware.fusion.tools.darwinPre15.zip.tar'))
        except:
            print('Link didn\'t work, trying another one...')
            n += 1
            continue

        # Extract the tar to zip
        tar = tarfile.open(convertpath(dest + '/tools/com.vmware.fusion.tools.darwinPre15.zip.tar'), 'r')
        tar.extract('com.vmware.fusion.tools.darwinPre15.zip', path=convertpath(dest + '/tools/'))
        tar.close()

        # Extract the iso and sig files from zip
        cdszip = zipfile.ZipFile(convertpath(dest + '/tools/com.vmware.fusion.tools.darwinPre15.zip'), 'r')
        cdszip.extract('payload/darwinPre15.iso', path=convertpath(dest + '/tools/'))
        cdszip.extract('payload/darwinPre15.iso.sig', path=convertpath(dest + '/tools/'))
        cdszip.close()

        # Move the iso and sig files to tools folder
        shutil.move(convertpath(dest + '/tools/payload/darwinPre15.iso'),
                    convertpath(dest + '/tools/darwinPre15.iso'))
        shutil.move(convertpath(dest + '/tools/payload/darwinPre15.iso.sig'),
                    convertpath(dest + '/tools/darwinPre15.iso.sig'))

        # Cleanup working files and folders
        shutil.rmtree(convertpath(dest + '/tools/payload'), True)
        os.remove(convertpath(dest + '/tools/com.vmware.fusion.tools.darwinPre15.zip.tar'))
        os.remove(convertpath(dest + '/tools/com.vmware.fusion.tools.darwinPre15.zip'))
        success = True

if __name__ == '__main__':
    main()
