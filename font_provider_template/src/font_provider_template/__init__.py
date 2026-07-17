import os.path
from os import PathLike
from typing import Tuple

__all__ = ("get_fonts",)


def get_fonts() -> Tuple[Tuple[str, PathLike, PathLike, PathLike]]:
    """
    Entry point for qtawesome's font-provider plugin system.

    This package registers ``get_fonts`` under the ``qtawesome.font_providers``
    entry-point group (see ``pyproject.toml``). qtawesome discovers it via
    ``importlib.metadata.entry_points``, calls it with no arguments, and
    loads every font tuple it returns alongside its bundled fonts.

    Each tuple in the returned sequence is
    ``(prefix, ttf_filename, charmap_filename, directory)``:

    - ``prefix``: the namespace used to reference icons, e.g. ``'si.github'``.
    - ``ttf_filename`` / ``charmap_filename``: filenames of the font and its
      icon-name-to-glyph JSON charmap, both expected inside ``directory``.
    - ``directory``: absolute path containing those two files. Resolving it
      relative to ``__file__`` (as below) ensures it works regardless of
      where the package gets installed.

    Return multiple tuples here to register several fonts from one provider.
    """
    return (
        (
            "si",
            "simple-icons.ttf",
            "simple-icons-charmap.json",
            os.path.join(os.path.dirname(__file__), "si"),
        ),
    )
