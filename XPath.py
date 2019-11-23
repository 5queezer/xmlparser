import sys
from io import StringIO
import xml.etree.ElementTree as ET

class XPath:
    def __init__(self):
        self.stdin = sys.stdin
        self.raw = ''

    def readStdin(self):
        return self.stdin.readline()

    def loadFile(self, filename):
        infile = open(filename, "r")
        self.raw = infile.read()
        return self.raw

    def loadXML(self, raw):
        self.root = ET.fromstring(raw)
        return self.root
