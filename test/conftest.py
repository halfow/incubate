import os
from pathlib import Path

import pytest


class TempLocation:
    def __init__(self, path: Path):
        self.path = path
        self.start = path.cwd()

    def __enter__(self):
        os.chdir(self.path)
        return self.path

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.chdir(self.start)


@pytest.fixture
def tmp_location(tmp_path):
    with TempLocation(tmp_path) as path:
        yield path
