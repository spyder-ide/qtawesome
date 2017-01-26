r"""
Tests for QtAwesome
"""
# Standard library imports
import subprocess

# Test Library imports
import pytest

def test_segfault_import():
    subprocess.call('python -c qtawesome')
    
if __name__ == "__main__":
    pytest.main()