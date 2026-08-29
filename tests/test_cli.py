import pytest
from pathlib import Path
from unittest.mock import patch
from forg.cli import main, run_organizer

def test_run_organizer_invalid_strategy(tmp_path):
    with pytest.raises(ValueError) as exc_info:
        run_organizer(tmp_path, strategy="invalid")
    assert "Unknown organization strategy: 'invalid'." in str(exc_info.value)
    assert "file" in str(exc_info.value)
    assert "size" in str(exc_info.value)

def test_main_parser_missing_command(monkeypatch):
    monkeypatch.setattr("sys.argv", ["forg"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0

def test_main_parser_invalid_strategy(monkeypatch, tmp_path):
    monkeypatch.setattr("sys.argv", ["forg", "run", str(tmp_path), "-o", "invalid"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0

@patch("forg.cli.run_organizer")
def test_main_run_success(mock_run_organizer, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["forg", "run", str(tmp_path), "-o", "date"])
    main()
    mock_run_organizer.assert_called_once_with(Path(tmp_path), "date")
    captured = capsys.readouterr()
    assert f"Sucessfully organized '{tmp_path}' by 'date' strategy" in captured.out

@patch("forg.cli.run_organizer")
def test_main_run_default_success(mock_run_organizer, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["forg", "run", str(tmp_path)])
    main()
    mock_run_organizer.assert_called_once_with(Path(tmp_path), "file")
    captured = capsys.readouterr()
    assert f"Sucessfully organized '{tmp_path}' by 'file' strategy" in captured.out

@patch("forg.cli.run_organizer")
def test_main_run_option_success(mock_run_organizer, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["forg", "run", str(tmp_path), "-o", "date"])
    main()
    mock_run_organizer.assert_called_once_with(Path(tmp_path), "date")
    captured = capsys.readouterr()
    assert f"Sucessfully organized '{tmp_path}' by 'date' strategy" in captured.out

@patch("forg.cli.run_organizer", side_effect=FileNotFoundError("Directory not found"))
def test_main_run_file_not_found(mock_run_organizer, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["forg", "run", "fake"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Error: Directory not found" in captured.err

@patch("forg.cli.run_organizer", side_effect=NotADirectoryError("Not a directory"))
def test_main_run_file_not_found(mock_run_organizer, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["forg", "run", "fake.txt"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Error: Not a directory" in captured.err
