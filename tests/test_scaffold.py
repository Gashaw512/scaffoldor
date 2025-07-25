import shutil
from pathlib import Path
import pytest
from scaffoldor.scaffold import create_structure

TEST_DIR = Path("test_project")

def teardown_function():
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)

def test_create_structure_creates_dirs():
    create_structure(TEST_DIR, dry_run=False)
    assert (TEST_DIR / "backend" / "app" / "api/v1").exists()
    assert (TEST_DIR / "frontend" / "src" / "components").exists()
    assert (TEST_DIR / ".env.example").exists()
    shutil.rmtree(TEST_DIR)

def test_create_structure_dry_run():
    create_structure(TEST_DIR, dry_run=True, verbose=True)
    assert not TEST_DIR.exists()
