import pytest
from XPath import XPath
from unittest.mock import MagicMock
from io import StringIO
import sys

contents = "<div></div>\n"

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
def test_CanReadFromStdin(mock_stdin):
    xpath = XPath()
    result = xpath.readStdin()
    mock_stdin.assert_called_once()
    assert result == contents

def test_CanReadFromFile(mock_open):
    xpath = XPath()
    result = xpath.readFile("foo.txt")
    mock_open.assert_called_once_with("foo.txt", "r")
    assert result == contents

def test_CanLoadInputIntoXMLParser(monkeypatch):
    pass