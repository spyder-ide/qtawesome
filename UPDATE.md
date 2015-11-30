To update font-awesome or elusive icons, one must

- replace the ttf font file with the new version
- regenerate the json charmap with the `icons.yml` file from the upstream
  repository:

````Python
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
