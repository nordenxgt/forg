import pytest
import platform
import subprocess
from unittest.mock import patch
from pathlib import Path
from forg.utils import st_ltime, file_ext, file_ctime, file_ord, file_size

@patch("subprocess.run")
def test_st_ltime_success(tmp_path):
    dummy_file = tmp_path / "test.txt"
    mock_subprocess.return_value.stdout = "1700000000\n"
    assert st_ltime(dummy_file) == 1700000000.0
    mock_subprocess.assert_called_once()

def test_st_ltime_success(tmp_path):
    dummy_file = tmp_path / "test.txt"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "1700000000\n"
        result = st_ltime(dummy_file)
        assert result == 1700000000.0
        mock_run.assert_called_once()

def test_st_ltime_success(tmp_path):
    dummy_file = tmp_path / "test.txt"
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "-\n"
        with pytest.raises(ValueError) as exc_info:
            st_ltime(dummy_file)
        assert "Birth time/Creation date not supported" in str(exc_info.value)
        mock_run.return_value.stdout = "0\n"
        with pytest.raises(ValueError) as exc_info:
            st_ltime(dummy_file)
        assert "Birth time/Creation date not supported" in str(exc_info.value)

def test_file_ext():
    extensions = {".txt": "Text", ".jpg": "Images", ".mid": "Audio"}
    assert file_ext("report.TXT", extensions) == "Text"
    assert file_ext("photo.jpg", extensions) == "Images"
    assert file_ext("audio.mp3", extensions) is None

@patch("platform.system")
def test_file_ctime_windows(mock_system, tmp_path):
    mock_system.return_value = "Windows"
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("hello")
    with patch.object(Path, "stat") as mock_stat:
        mock_stat.return_value.st_ctime = 123456.78
        assert file_ctime(dummy_file) == 123456.78

@patch("platform.system")
def test_file_ctime_darwin(mock_system, tmp_path):
    mock_system.return_value = "Darwin"
    dummy_file = tmp_path / "test.txt"
    dummy_file.write_text("hello")
    with patch.object(Path, "stat") as mock_stat:
        mock_stat.return_value.st_birthtime = 1710000000.0
        assert file_ctime(dummy_file) == 1710000000.0

@patch("platform.system")
@patch("subprocess.run")
def test_file_ctime_linux(mock_subprocess, mock_system, tmp_path):
    mock_system.return_value = "Linux"
    mock_subprocess.return_value.stdout = "1720000000\n"
    dummy_file = tmp_path / "test.txt"
    assert file_ctime(dummy_file) == 1720000000.0
    mock_subprocess.assert_called_once()

def test_file_ord():
    assert file_ord("apple.py") == "A-K"
    assert file_ord("Lemon.txt") == "L-U"
    assert file_ord("zebra.py") == "V-Z"
    assert file_ord("12.txt") == "Others"

def test_file_size(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"0000000000") # 10 bytes
    assert file_size(Path(file_path), 10.0) == "Small"
    assert file_size(Path(file_path), 5.0) == "Medium"
    assert file_size(Path(file_path), 4.0) == "Large"
