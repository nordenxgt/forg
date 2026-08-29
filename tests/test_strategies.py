import pytest
import json
from pathlib import Path
from unittest.mock import patch
from forg.strategies import ofile, odate, oname, osize, move_file, strategy

def test_strategy_invalid_directory():
    dummy_dir = Path("/dummy")
    with pytest.raises(FileNotFoundError):
        strategy(dummy_dir, lambda d, c, f: None)

def test_strategy_is_not_a_directory(tmp_path):
    dummy_file = tmp_path / "file.txt"
    dummy_file.touch()
    with pytest.raises(NotADirectoryError):
        strategy(dummy_file, lambda d, c, f: None)

def test_move_file_success(tmp_path):
    sub_dir = tmp_path / "sub_dir"
    sub_dir.mkdir()
    file_path = sub_dir / "test.txt"
    file_path.write_text("Hello")
    move_file(tmp_path, sub_dir, "test.txt", "Text")
    assert not file_path.exists()
    assert (tmp_path / "Text" / "test.txt").read_text() == "Hello"

def test_move_duplicate_file_success(tmp_path):
    target_dir = tmp_path / "Text"
    target_dir.mkdir()
    (target_dir / "test.txt").write_text("old")

    sub_dir = tmp_path / "source"
    sub_dir.mkdir()
    file_path = sub_dir / "test.txt"
    file_path.write_text("new")
    move_file(tmp_path, sub_dir, "test.txt", "Text")
    assert (target_dir / "test.txt").read_text() == "old"
    assert (target_dir / "test_1.txt").read_text() == "new"

def test_ofile_missing_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="json file is missing"):
        ofile(tmp_path)
    # with pytest.raises(FileNotFoundError) as exc_info:
    #    ofile(tmp_path)
    # assert "json file is missing" in str(exc_info.value)

def test_ofile_success(tmp_path):
    ext_json = tmp_path / "extensions.json"
    ext_json.write_text(json.dumps({"txt": "Text"}))
    (tmp_path / "note.txt").write_text("text")
    ofile(tmp_path)
    assert (tmp_path / "Text" / "note.txt").exists()

@patch("forg.strategies.file_ctime")
def test_odate_success(mock_file_ctime, tmp_path):
    test_file = tmp_path / "photo.jpg"
    test_file.write_bytes(b"image")
    mock_file_ctime.return_value = 1720000000.0
    odate(tmp_path)
    subdirs = [p.name for p in tmp_path.iterdir() if p.is_dir()]
    assert len(subdirs) == 1
    date_folder = tmp_path / subdirs[0]
    assert (date_folder / "photo.jpg").exists()

def test_oname_success(tmp_path):
    (tmp_path / "apple.txt").write_text("a")
    (tmp_path / "zebra.txt").write_text("z")
    oname(tmp_path)
    assert (tmp_path / "A-K" / "apple.txt").exists()
    assert (tmp_path / "V-Z" / "zebra.txt").exists()

def test_osize_success(tmp_path):
    (tmp_path / "small.txt").write_bytes(b"a")
    (tmp_path / "medium.txt").write_bytes(b"abcdefghij")
    osize(tmp_path)
    subdirs = [p.name for p in tmp_path.iterdir() if p.is_dir()]
    assert len(subdirs) > 0
