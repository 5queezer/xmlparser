import pytest
from XPath import XPath
from unittest.mock import MagicMock
from io import StringIO
import sys
import xml.etree.ElementTree as ET

contents = "<div><a></a><a></a></div>\n"

@pytest.fixture
def xpath():
    return XPath()

@pytest.fixture
def mock_stdin(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value=contents)
    mock_stdin = MagicMock(return_value=mock_file)
    monkeypatch.setattr("sys.stdin", mock_open)
    print("\nfile open")
    yield mock_stdin
    print("\nfile close")

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
    root = xpath.loadXML(raw)
    assert root.tag == ET.fromstring(contents).tag
