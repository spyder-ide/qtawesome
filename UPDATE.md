# How to update font packs

## FontAwesome

To update _FontAwesome_ icons, one must:

- check what is the latest released version here: https://github.com/FortAwesome/Font-Awesome/releases/
- run: python setup.py update_fa5 --fa-version X.X.X
- update FA version number, icon counts and URLs inside:
  - README.md
  - qtawesome/docs/source/usage.rst

## Elusive Icons

To update _Elusive Icons_, one must:

- replace the ttf font file with the new version
- regenerate the json charmap with the `icons.yml` file from the upstream repository:

```Python
import yaml, json

with open('icons.yml', 'r') as file:
    icons = yaml.load(file)['icons']

charmap = {icon['id']: icon['unicode'] for icon in icons}

for icon in icons:
    if 'aliases' in icon:
        for name in icon['aliases']:
            charmap[name] = icon['unicode']

with open('charmap.json', 'w') as file:
    json.dump(charmap, file, indent=4, sort_keys=True)
```

## Material Design Icons

To update _Material Design Icons_, you must:

- download ttf from https://github.com/Templarian/MaterialDesign-Webfont
- regenerate the json charmap with the `materialdesignicons.css` file.

```Python
import re
import json

with open('css/materialdesignicons.css', 'r') as fp:
    rawcss = fp.read()

charmap = {}
pattern = '^\.mdi-(.+):before {\s*content: "(.+)";\s*}$'
data = re.findall(pattern, rawcss, re.MULTILINE)
for name, key in data:
    key = key.replace('\\F', '0xf').lower()
    key = key.replace('\\', '0x')
    name = name.lower()
    charmap[name] = key

with open('materialdesignicons-webfont-charmap.json', 'w') as fp:
    json.dump(charmap, fp, indent=4, sort_keys=True)
```
