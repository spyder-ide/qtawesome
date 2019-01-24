r"""
Tests for QtAwesome.
"""
# Standard library imports
import sys
import subprocess

# Test Library imports
import pytest

# Local imports
import qtawesome as qta
from qtawesome.iconic_font import IconicFont
from PyQt5.QtWidgets import QApplication


def test_segfault_import():
    output_number = subprocess.call('python -c "import qtawesome '
                                    '; qtawesome.icon()"', shell=True)
    assert output_number == 0


def test_unique_font_family_name():
    """
    Test that each font used by qtawesome has a unique name. If this test
    fails, this probably means that you need to rename the family name of
    some fonts. Please see PR #98 for more details on why it is necessary and
    on how to do this.

    Regression test for Issue #107
    """
    app = QApplication(sys.argv)

    resource = qta._instance()
    assert isinstance(resource, IconicFont)

    prefixes = list(resource.fontname.keys())
    assert prefixes

    fontnames = set(resource.fontname.values())
    assert fontnames

    assert len(prefixes) == len(fontnames)

    sys.exit(app.exec_())


if __name__ == "__main__":
    pytest.main()
