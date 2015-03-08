import json
import os
    
from .iconic_font import IconicFont

_res = { 'iconic' : None, }

def _instance():
    if _res['iconic'] is None:
        _res['iconic'] =  IconicFont('fontawesome-4.3.0.ttf', 'fontawesome-4.3.0-charmap.json')
    return _res['iconic']

def charmap(arg):
    return _instance().charmap[arg]

def icon(*args, **kwargs):     
    return _instance().icon_by_name(*args, **kwargs)

def font(*args, **kwargs):     
    return _instance().font(*args, **kwargs)

def icon_by_char(*args, **kwargs):    
    return _instance().icon_by_char(*args, **kwargs)

def give(*args, **kwargs):
    return _instance().give(*args, **kwargs)