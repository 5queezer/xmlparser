import sys
from io import StringIO

class XPath:
    def __init__(self):
        self.stdin = sys.stdin

    def readStdin(self):
        return self.stdin.read()

    def readFile(self, filename):
        infile = open(filename, "r")
        raw = infile.read()
        return raw

