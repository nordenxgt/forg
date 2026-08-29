import pytest
from pathlib import Path
from unittest.mock import patch
from forg.service import run_organizer

def test_run_organizer_invalid_strategy(tmp_path):
    with pytest.raises(ValueError) as exc_info:
        run_organizer(tmp_path, strategy="invalid")
    assert "Unknown organization strategy: 'invalid'." in str(exc_info.value)
    assert "file" in str(exc_info.value)
    assert "size" in str(exc_info.value)

