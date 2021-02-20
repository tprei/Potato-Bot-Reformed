import json
import os

class EmptyFileError(Exception):
    pass

def load(file_name):
    with open(file_name, encoding="UTF-8") as json_data:
        GLOBAL = json.load(json_data) 

    return GLOBAL

def export(dictionary, file_name):
    if len(dictionary) == 0:
        raise EmptyFileError('dictionary is empty, are you doing the right thing?')
    
    with open(file_name, 'w') as json_data:
        json.dump(dictionary, json_data, indent=4, sort_keys=True)

def add_global(p, q, file_name='utils/resources/config.json', append=False):
    if p in GLOBAL and (q == GLOBAL[p] or (append and q in GLOBAL[p])):
        return

    if append:
        GLOBAL[p].append(q)
    else:
        GLOBAL[p] = q

    export(GLOBAL, file_name)

def remove_global(p, file_name='utils/resources/config.json'):
    GLOBAL.pop(p, None)
    export(GLOBAL, file_name)

def remove_entry(p, q, file_name='utils/resources/config.json'):
    if p not in GLOBAL:
        return
    elif q not in GLOBAL[p]:
        return

    GLOBAL[p].remove(q)
    export(GLOBAL, file_name)

GLOBAL = load('utils/resources/config.json')
EMOJI = load('utils/resources/emoji.json')
