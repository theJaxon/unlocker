import os
import urllib
import urllib2
from HTMLParser import HTMLParser
import shutil
import tarfile
import zipfile


# Parse the Fusion directory page
class myHTMLParser(HTMLParser):

    def __init__(self):
        self.reset()
        self.HTMLDATA = []

    def handle_data(self, data):
        if data.find("\n") == -1 :
            if data[0].isdigit():
                self.HTMLDATA.append(data)

    def clean(self):
        self.HTMLDATA = []


def main():
    url = 'http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/'
    dir = os.path.dirname(os.path.abspath(__file__))
    response = urllib2.urlopen(url)
    html = response.read()
    parser = myHTMLParser()
    parser.feed(html)
    url = url + parser.HTMLDATA[-1] + '/'
    response = urllib2.urlopen(url)
    html = response.read()
    parser.clean()
    parser.feed(html)
    url = url + parser.HTMLDATA[-1] + '/packages/com.vmware.fusion.tools.darwin.zip.tar'
    urllib.urlretrieve(url, 'tools/com.vmware.fusion.tools.darwin.zip.tar')
    parser.clean()
    tar = tarfile.open('tools/com.vmware.fusion.tools.darwin.zip.tar', 'r')
    tar.extract('com.vmware.fusion.tools.darwin.zip', path='tools/')
    zip = zipfile.ZipFile('tools/com.vmware.fusion.tools.darwin.zip', 'r')
    zip.extract('payload/darwin.iso', path='tools/')
    zip.extract('payload/darwin.iso.sig', path='tools/')
    shutil.move(dir + '/tools/payload/darwin.iso', dir + '/tools/darwin.iso')
    shutil.move(dir + '/tools/payload/darwin.iso.sig', dir + '/tools/darwin.iso.sig')
    shutil.rmtree(dir +  '/tools/payload', True)
    os.remove(dir + '/tools/com.vmware.fusion.tools.darwin.zip.tar')
    os.remove(dir + '/tools/com.vmware.fusion.tools.darwin.zip')


if __name__ == '__main__':
    main()
