import pytest
from pathlib import Path
from unittest.mock import patch
from forg.service import run_organizer

def test_run_organizer_invalid_strategy(tmp_path):
    with pytest.raises(ValueError) as exc_info:
        run_organizer(tmp_path, strategy="invalid")
    assert "Unknown organization strategy: 'invalid'." in str(exc_info.value)

@patch("forg.service.ofile")
def test_run_organizer_file_strategy(mock_ofile, tmp_path):
    run_organizer(tmp_path, strategy="file")
    mock_ofile.assert_called_once_with(tmp_path)

@patch("forg.service.oname")
def test_run_organizer_file_strategy(mock_oname, tmp_path):
    run_organizer(tmp_path, strategy="name")
    mock_oname.assert_called_once_with(tmp_path)

@patch("forg.service.odate")
def test_run_organizer_file_strategy(mock_odate, tmp_path):
    run_organizer(tmp_path, strategy="time")
    mock_odate.assert_called_once_with(tmp_path)

@patch("forg.service.osize")
def test_run_organizer_file_strategy(mock_osize, tmp_path):
    run_organizer(tmp_path, strategy="size")
    mock_osize.assert_called_once_with(tmp_path)
