import pytest
from XPath import XPath
from unittest.mock import MagicMock
from io import StringIO
import sys
import xml.etree.ElementTree as ET

# contents = "<div><a></a><a></a></div>\n"
contents = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
"""

def elements_equal(e1, e2):
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

@pytest.fixture
def xpath():
    return XPath()

@pytest.fixture
def mock_stdin(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value=contents)
    mock_stdin = MagicMock(return_value=mock_file)
    monkeypatch.setattr("sys.stdin", mock_open)
    print("\nstdin open")
    yield mock_stdin
    print("\nstdin close")

@pytest.fixture
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.read = MagicMock(return_value=contents)
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    print("\nfile open")
    yield mock_open
    print("\nfile close")

@pytest.mark.skip
def test_CanReadFromStdin(xpath, mock_stdin):
    result = xpath.readStdin()
    mock_stdin.assert_called_once()
    assert result == contents

def test_CanReadFromFile(xpath, mock_open):
    result = xpath.loadFile("foo.txt")
    mock_open.assert_called_once_with("foo.txt", "r")
    assert result == contents

def test_CanLoadInputIntoXMLParser(xpath, mock_open):
    raw = xpath.loadFile("foo.txt")
    mock_open.assert_called_once_with("foo.txt", "r")
    xpath.loadXML(raw)
    assert xpath.root.tag == ET.fromstring(contents).tag

def test_CanOutputXML(xpath, mock_open):
    raw = xpath.loadFile("foo.txt")
    mock_open.assert_called_once_with("foo.txt", "r")
    xpath.loadXML(raw)
    output = xpath.toXML()
    assert elements_equal(ET.fromstring(output), ET.fromstring(contents))
