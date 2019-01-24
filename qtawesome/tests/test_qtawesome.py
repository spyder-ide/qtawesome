r"""
Tests for QtAwesome.
"""
# Standard library imports
import subprocess

# Test Library imports
import pytest

# Local imports
import qtawesome as qta
from qtawesome.iconic_font import IconicFont


def test_segfault_import():
    output_number = subprocess.call('python -c "import qtawesome '
                                    '; qtawesome.icon()"', shell=True)
    assert output_number == 0


def test_unique_font_family_name(qtbot):
    """
    Test that each font used by qtawesome has a unique name.

    Regression test for Issue #107
    """
    resource = qta._instance()
    assert isinstance(resource, IconicFont)

    prefixes = list(resource.fontname.keys())
    assert prefixes

    fontnames = set(resource.fontname.values())
    assert fontnames

    assert len(prefixes) == len(fontnames)


if __name__ == "__main__":
    pytest.main()
