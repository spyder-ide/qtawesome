To update font-awesome or elusive icons, one must

- replace the TTF or OTF font file with the new version
- regenerate the JSON charmap with the `icons.yml` file from the upstream's /advanced-options/metadata
  repository using update.py
- update icons' names and aliases using shims.py and shims.json
