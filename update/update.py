
import yaml, json

with open('icons.yml', 'r') as file:
    icons = yaml.load(file)

charmap = {icon: icons[icon]['unicode'] for icon in icons}

with open('charmap.json', 'w') as file:
    json.dump(charmap, file, indent=4, sort_keys=True)

