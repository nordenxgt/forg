import pytest
import random
import json
from pathlib import Path
from forg.cli import ofile

def test_ofile_raises_file_not_found():
    fake_path = Path("/fake")
    with pytest.raises(FileNotFoundError) as exc_info:
        ofile(fake_path)
    assert "does not exist" in str(exc_info.value)

def test_ofile_raises_not_a_directory(tmp_path):
    fake_path = tmp_path/"fake.txt"
    fake_path.touch() 
    with pytest.raises(NotADirectoryError) as exc_info:
        ofile(fake_path)
    assert "is not a valid directory" in str(exc_info.value)

def test_ofile_success(tmp_path):
    sub_dir = tmp_path/"sub_dir"
    sub_dir.mkdir()

    file_txt = tmp_path/"a.txt"
    file_jpg = sub_dir/"b.jpg"
    file_gz = tmp_path/"c.gz"
    file_txt.write_text("Testing ofile")
    file_jpg.write_bytes(b"jpg")
    file_gz.touch()

    ofile(tmp_path)

    with open("extensions.json", "r", encoding="utf-8") as f: 
        extensions = json.load(f)
    assert not file_txt.exists()
    assert not file_jpg.exists()
    assert not file_gz.exists()
    assert (tmp_path/extensions[".txt"]/"a.txt").exists()
    assert (tmp_path/extensions[".jpg"]/"b.jpg").exists()
    assert (tmp_path/extensions[".gz"]/"c.gz").exists()

def test_ofile_ignores_unknown_extensions(tmp_path):
    unknown_file = tmp_path / "file.unknown"
    unknown_file.write_text("hello")
    ofile(tmp_path)
    assert unknown_file.exists()
    assert unknown_file.read_text() == "hello"
