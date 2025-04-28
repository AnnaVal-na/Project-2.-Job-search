import pytest
from src.storage import JSONStorage
from pathlib import Path

@pytest.fixture
def temp_storage(tmp_path):
    """Фикстура для временного хранилища"""
    return JSONStorage(filename=tmp_path / 'test.json')
