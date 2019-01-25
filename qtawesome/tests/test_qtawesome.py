r"""
Tests for QtAwesome.
"""
# Standard library imports
import subprocess
import collections

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
    Test that each font used by qtawesome has a unique name. If this test
    fails, this probably means that you need to rename the family name of
    some fonts. Please see PR #98 for more details on why it is necessary and
    on how to do this.

    Regression test for Issue #107
    """
    resource = qta._instance()
    assert isinstance(resource, IconicFont)

    # Check that the fonts were loaded successfully.
    fontnames = resource.fontname.values()
    assert fontnames

    # Check that qtawesome does not load fonts with duplicate family names.
    duplicates = [fontname for fontname, count in
                  collections.Counter(fontnames).items() if count > 1]
    assert not duplicates


if __name__ == "__main__":
    pytest.main()
