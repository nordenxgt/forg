import pytest
from pathlib import Path
from forg.cli import ofile, FILE_ORGANIZATION

def test_ofile_raises_file_not_found():
    fake_path = Path("/fake")
    with pytest.raises(FileNotFoundError) as e:
        ofile(fake_path)
    assert "does not exist" in str(e.value)

def test_ofile_raises_not_a_directory(tmp_path):
    fake_path = tmp_path/"fake.txt"
    fake_path.touch() 
    with pytest.raises(NotADirectoryError) as exc_info:
        ofile(fake_path)
    assert "is not a valid directory" in str(exc_info.value)

def test_ofile_success(tmp_path):
    sub_dir = tmp_path/"sub_dir"
    sub_dir.mkdir()

    file_txt = tmp_path / "a.txt"
    file_jpg = sub_dir / "b.jpg"
    file_mp3 = sub_dir / "c.mp3"
    file_mp4 = tmp_path / "d.mp4"
    file_unknown = sub_dir / "e.pdf"

    file_txt.touch()
    file_jpg.touch()
    file_mp3.touch()
    file_mp4.touch()
    file_unknown.touch()

    ofile(tmp_path)

    assert not file_txt.exists()
    assert not file_jpg.exists()
    assert not file_mp3.exists()
    assert not file_mp4.exists()

    assert file_unknown.exists()
    assert (tmp_path / FILE_ORGANIZATION[0] / "a.txt").exists()
    assert (tmp_path / FILE_ORGANIZATION[1] / "b.jpg").exists()
    assert (tmp_path / FILE_ORGANIZATION[2] / "c.mp3").exists()
    assert (tmp_path / FILE_ORGANIZATION[3] / "d.mp4").exists()
