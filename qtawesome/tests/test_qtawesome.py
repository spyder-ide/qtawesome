r"""
Tests for QtAwesome.
"""
# Standard library imports
import subprocess

# Test Library imports
import pytest

def test_segfault_import():
    output_number = subprocess.call('python -c "import qtawesome '
                                    '; qtawesome.icon()"', shell=True)
    assert output_number == 0
    
if __name__ == "__main__":
    pytest.main()
