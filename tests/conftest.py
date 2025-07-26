# tests/conftest.py
import pytest
from pathlib import Path
import sys
import shutil

# This fixture is useful for ensuring clean tests by
# redirecting stdout to capture it without affecting actual console output during tests.
# It's less crucial now with logging, but good practice for CLI tools.
@pytest.fixture(autouse=True)
def capsys_strict(capsys):
    """
    A pytest fixture that ensures stdout and stderr are strictly captured
    and resets them after each test.
    """
    yield capsys
    # After the test, clean up any remaining output
    sys.stdout.seek(0)
    sys.stderr.seek(0)
    sys.stdout.truncate(0)
    sys.stderr.truncate(0)


@pytest.fixture
def tmp_project_dir(tmp_path: Path):
    """
    Provides a temporary directory for project creation tests.
    Ensures a clean slate for each test by yielding a unique path.
    """
    yield tmp_path
    # Cleanup is handled by tmp_path fixture itself