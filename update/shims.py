import json
import os

shimsfile=os.path.join(os.path.dirname(__file__), 'shims.json')
with open(shimsfile) as shims_json:
    shims_dict = json.load(shims_json)

shims = {'fa.' + nmchg[0]: ".".join([nmchg[1], nmchg[2]]) if nmchg[1] else "fas." + nmchg[2]
         for nmchg in shims_dict if nmchg[2]}


def update_fa_name(icon):
    # change name if it was updated or moved to another OTF
    if icon in shims:
        newname = shims[icon]
    # otherwise, only change the prefix to Solid (which is supposed to be default)
    else:
        newname = icon.replace("fa.", "fas.")
    return newname


def update_fa_dict(namedict):
    """
    Icon names require updating due to Font Awesome's 5 name changes and splitting of OTFs
    :param namedict: dictionary with aliases for icons, like Spyder's icon_manager.py
    :param shims: rules for name changing obtained from Font Awesome's shims.json
    :return: modifies the dictionary in plase
    """
    for name in namedict:
        icons, *decor = namedict[name]
        newicons = []
        for icon in icons:
            newicons.append(update_fa_name(icon))
        namedict[name] = [tuple(newicons), *decor]
