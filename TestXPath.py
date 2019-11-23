import pytest
from XPath import XPath
from unittest.mock import MagicMock
from io import StringIO
import sys

contents = "<div></div>\n"


@pytest.fixture
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.read = MagicMock(return_value=contents)
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open

@pytest.mark.skip
def test_CanReadFromStdin(monkeypatch):
    xpath = XPath()
    monkeypatch.setattr(sys, 'stdin', StringIO(contents))
    assert xpath.readStdin() == contents

def test_CanReadFromFile(mock_open, monkeypatch):
    xpath = XPath()
    result = xpath.readFile("foo.txt")
    mock_open.assert_called_once_with("foo.txt", "r")
    assert result == contents

def test_CanLoadInputIntoXMLParser(monkeypatch):
    pass