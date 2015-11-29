"""
The MIT License (MIT)

Copyright (c) 2015 Dave Parsons

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

import os
import sys
import urllib
import urllib2
from HTMLParser import HTMLParser
import shutil
import tarfile
import zipfile


# Parse the Fusion directory page
class myHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.reset()
        self.HTMLDATA = []

    def handle_data(self, data):
        # Build a list of numeric data from any element
        if data.find("\n") == -1 :
            if data[0].isdigit():
                self.HTMLDATA.append(data)

    def clean(self):
        self.HTMLDATA = []


def convertPath(path):
    # OS path separator replacement funciton
    return path.replace(os.path.sep, '/')


def main():

    # Check minimal Python version is 2.7
    if sys.version_info < (2, 7):
        sys.stderr.write('You need Python 2.7 or later\n')
        sys.exit(1)

    # Setup url and file paths
    url = 'http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/'
    dir = os.path.dirname(os.path.abspath(__file__))

    # Re-create the tools folder
    shutil.rmtree(dir + '/tools', True)
    os.mkdir(dir + '/tools')

    # Get the list of Fusion releases
    # And get the last item in the ul/li tags
    response = urllib2.urlopen(url)
    html = response.read()
    parser = myHTMLParser()
    parser.feed(html)
    url = url + parser.HTMLDATA[-1] + '/'
    parser.clean()

    # Open the latest release page
    # And build file URL
    response = urllib2.urlopen(url)
    html = response.read()
    parser.feed(html)
    url = url + parser.HTMLDATA[-1] + '/packages/com.vmware.fusion.tools.darwin.zip.tar'
    parser.clean()

    # Download the darwin.iso tgz file
    print 'Retrieving tools from: ' + url
    urllib.urlretrieve(url, convertPath(dir + '/tools/com.vmware.fusion.tools.darwin.zip.tar'))

    # Extract the tar to zip
    tar = tarfile.open(convertPath(dir + '/tools/com.vmware.fusion.tools.darwin.zip.tar'), 'r')
    tar.extract('com.vmware.fusion.tools.darwin.zip', path=convertPath(dir + '/tools/'))
    tar.close()

    # Extract the iso and sig files from zip
    zip = zipfile.ZipFile(convertPath(dir + '/tools/com.vmware.fusion.tools.darwin.zip'), 'r')
    zip.extract('payload/darwin.iso', path=convertPath(dir + '/tools/'))
    zip.extract('payload/darwin.iso.sig', path=convertPath(dir + '/tools/'))
    zip.close()

    # Move the iso and sig files to tools folder
    shutil.move(convertPath(dir + '/tools/payload/darwin.iso'), convertPath(dir + '/tools/darwin.iso'))
    shutil.move(convertPath(dir + '/tools/payload/darwin.iso.sig'), convertPath(dir + '/tools/darwin.iso.sig'))

    # Cleanup working files and folders
    shutil.rmtree(convertPath(dir + '/tools/payload'), True)
    os.remove(convertPath(dir + '/tools/com.vmware.fusion.tools.darwin.zip.tar'))
    os.remove(convertPath(dir + '/tools/com.vmware.fusion.tools.darwin.zip'))


if __name__ == '__main__':
    main()
