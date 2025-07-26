import subprocess
import sys

def test_version_flag():
    result = subprocess.run([sys.executable, "-m", "scaffoldor.cli", "--version"], capture_output=True, text=True)
    assert "scaffoldor version" in result.stdout
