# font_provider_template

Template for a package that provides extra iconic fonts to
[qtawesome](https://github.com/spyder-ide/qtawesome) via its
font-provider plugin system.

## Testing this template

```bash
git clone https://github.com/o-murphy/qtawesome -b feat/font_providers
cd qtawesome
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
pip install -e font_provider_template
qta-browser  # the 'si' prefix will be available
```

## How it works

qtawesome bundles a fixed set of icon fonts (Font Awesome, Material Design
Icons, Phosphor, etc.), but third-party packages can register additional
fonts without qtawesome needing to know about them in advance. This is done
through a Python entry point in the `qtawesome.font_providers` group.

At startup, qtawesome:

1. Looks up every entry point registered in the `qtawesome.font_providers`
   group via `importlib.metadata.entry_points`.
2. Loads and calls each one (no arguments).
3. Loads every font tuple each call returns, in addition to its own bundled
   fonts.

## Structure of this template

- [`pyproject.toml`](pyproject.toml) registers the entry point:

  ```toml
  [project.entry-points."qtawesome.font_providers"]
  qtmdi_icons = "font_provider_template:get_fonts"
  ```

  The key (`qtmdi_icons`) is just a unique identifier for the entry point
  itself and has no effect on icon lookup; only the target
  (`font_provider_template:get_fonts`) matters — it must point to an
  importable, no-argument callable.

- [`src/font_provider_template/__init__.py`](src/font_provider_template/__init__.py)
  defines `get_fonts()`, which returns a tuple of font tuples:

  ```python
  (prefix, ttf_filename, charmap_filename, directory)
  ```

  - `prefix`: namespace used when referencing icons, e.g. `qta.icon('si.github')`.
  - `ttf_filename`: the `.ttf` font file, expected inside `directory`.
  - `charmap_filename`: a JSON file mapping icon names to unicode glyphs,
    also expected inside `directory`.
  - `directory`: absolute path containing both files above. Resolve it
    relative to `__file__` so it works no matter where the package is
    installed.

  A single provider can return more than one tuple to register several
  fonts at once.

- `si/` contains the actual font and charmap files bundled with this
  example package (`simple-icons.ttf`, `simple-icons-charmap.json`).

## License

This template's own code (`LICENSE.txt`) is MIT-licensed, same as
qtawesome itself.

The bundled `si/simple-icons.ttf` and `si/simple-icons-charmap.json` are
derived from the [Simple Icons](https://simpleicons.org) project and are
licensed separately under **CC0 1.0 Universal** — see
[`src/font_provider_template/licenses/CC0-1.0-simple-icons.md`](src/font_provider_template/licenses/CC0-1.0-simple-icons.md).
Note that CC0 covers the icon designs only: the brand names and logos
depicted by individual icons remain trademarks of their respective owners,
and CC0 does not grant any trademark rights.

If you replace `si/` with a different font in your own provider package,
make sure to swap in that font's actual license and update this section
accordingly — don't keep the CC0 notice for a font it doesn't apply to.

## Using this template

1. Rename the package (`font_provider_template` in both the directory name
   and `pyproject.toml`'s `[project].name`) and the entry-point key
   (`qtmdi_icons`) to something specific to your font.
2. Replace the contents of `si/` with your own `.ttf` and charmap JSON.
3. Update `get_fonts()` to return the correct `prefix`, filenames, and
   tuple(s) for your font(s).
4. Build and install the package (e.g. `uv build`, then `pip install
   dist/*.whl`) — qtawesome will pick up the fonts automatically the next
   time it initializes, no code changes needed on the qtawesome side.
