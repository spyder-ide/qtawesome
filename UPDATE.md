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

- download ttf from <https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/master/fonts/materialdesignicons-webfont.ttf>
- regenerate the json charmap with the `materialdesignicons.css` file from <https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/master/css/materialdesignicons.css>

The following script automatically download the last TTF font, generate the json charmap and display md5 hash of the TTF (to update iconic_font.py)

```Python
import re
import json
import urllib.request
import hashlib

TTF_URL = 'https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/master/fonts/materialdesignicons-webfont.ttf'
CSS_URL = 'https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/master/css/materialdesignicons.css'

with open('materialdesignicons-webfont.ttf', 'wb') as fp:
    req = urllib.request.urlopen(TTF_URL)
    if req.status != 200:
        raise Exception('Failed to download TTF')
    fp.write(req.read())
    req.close()

hasher = hashlib.md5()
with open('materialdesignicons-webfont.ttf', 'rb') as f:
    content = f.read()
    hasher.update(content)

ttf_calculated_hash_code = hasher.hexdigest()
print('MD5 :', ttf_calculated_hash_code)

req = urllib.request.urlopen(CSS_URL)
if req.status != 200:
    raise Exception('Failed to download CSS Charmap')

rawcss = req.read().decode()
req.close()

charmap = {}
pattern = '^\.mdi-(.+)::before {\s*content: "(.+)";\s*}$'
data = re.findall(pattern, rawcss, re.MULTILINE)
for name, key in data:
    key = key.replace('\\F', '0xf').lower()
    key = key.replace('\\', '0x')
    name = name.lower()
    charmap[name] = key

with open('materialdesignicons-webfont-charmap.json', 'w') as fp:
    json.dump(charmap, fp, indent=4, sort_keys=True)

```

## Phosphor

To update _Phosphor_, you must:

- download ttf from <https://raw.githubusercontent.com/phosphor-icons/phosphor-icons/master/src/font/phosphor.ttf>
- regenerate the json charmap with the `phosphor.css` file from <https://raw.githubusercontent.com/phosphor-icons/phosphor-icons/master/src/css/phosphor.css>

The following script automatically download the last TTF font, generate the json charmap and display md5 hash of the TTF (to update iconic_font.py)

```Python
import re
import json
import urllib.request
import hashlib

TTF_URL = 'https://raw.githubusercontent.com/phosphor-icons/phosphor-icons/master/src/font/phosphor.ttf'
CSS_URL = 'https://raw.githubusercontent.com/phosphor-icons/phosphor-icons/master/src/css/phosphor.css'

with open('phosphor.ttf', 'wb') as fp:
    req = urllib.request.urlopen(TTF_URL)
    if req.status != 200:
        raise Exception('Failed to download TTF')
    fp.write(req.read())
    req.close()

hasher = hashlib.md5()
with open('phosphor.ttf', 'rb') as f:
    content = f.read()
    hasher.update(content)

ttf_calculated_hash_code = hasher.hexdigest()
print('MD5 :', ttf_calculated_hash_code)

req = urllib.request.urlopen(CSS_URL)
if req.status != 200:
    raise Exception('Failed to download CSS Charmap')

rawcss = req.read().decode()
req.close()

charmap = {}
pattern = '^\.ph-(.+):before {\s*content: "(.+)";\s*}$'
data = re.findall(pattern, rawcss, re.MULTILINE)
for name, key in data:
    key = key.replace('\\', '0x')
    name = name.lower()
    charmap[name] = key

with open('phosphor-charmap.json', 'w') as fp:
    json.dump(charmap, fp, indent=4, sort_keys=True)

```

## Remix Icon

To update _Remix Icon_, you must:

- download ttf from <https://raw.githubusercontent.com/Remix-Design/RemixIcon/master/fonts/remixicon.ttf>
- regenerate the json charmap with the `remixicon.css` file from <https://raw.githubusercontent.com/Remix-Design/RemixIcon/master/fonts/remixicon.css>

The following script automatically download the last TTF font, generate the json charmap and display md5 hash of the TTF (to update iconic_font.py)

```Python
import re
import json
import urllib.request
import hashlib

TTF_URL = 'https://raw.githubusercontent.com/Remix-Design/RemixIcon/master/fonts/remixicon.ttf'
CSS_URL = 'https://raw.githubusercontent.com/Remix-Design/RemixIcon/master/fonts/remixicon.css'

with open('remixicon.ttf', 'wb') as fp:
    req = urllib.request.urlopen(TTF_URL)
    if req.status != 200:
        raise Exception('Failed to download TTF')
    fp.write(req.read())
    req.close()

hasher = hashlib.md5()
with open('remixicon.ttf', 'rb') as f:
    content = f.read()
    hasher.update(content)

ttf_calculated_hash_code = hasher.hexdigest()
print('MD5 :', ttf_calculated_hash_code)

req = urllib.request.urlopen(CSS_URL)
if req.status != 200:
    raise Exception('Failed to download CSS Charmap')

rawcss = req.read().decode()
req.close()

charmap = {}
pattern = '^\.ri-(.+):before {\s*content: "(.+)";\s*}$'
data = re.findall(pattern, rawcss, re.MULTILINE)
for name, key in data:
    key = key.replace('\\', '0x')
    name = name.lower()
    charmap[name] = key

with open('remixicon-charmap.json', 'w') as fp:
    json.dump(charmap, fp, indent=4, sort_keys=True)

```
