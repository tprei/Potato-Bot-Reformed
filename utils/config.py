import json
import os

class EmptyFileError(Exception):
    pass

def load(file_name):
    with open(file_name) as json_data:
        GLOBAL = json.load(json_data) 

    return GLOBAL

def export(dictionary, file_name):
    if len(dictionary) == 0:
        raise EmptyFileError('GLOBAL dictionary is empty, are you doing the right thing?')
    
    with open(file_name, 'w') as json_data:
        json.dump(dictionary, json_data)

def add_global(p, q, file_name='utils/config.json'):
    GLOBAL[p] = q
    export(GLOBAL, file_name)

def remove_global(p, file_name='utils/config.json'):
    GLOBAL.pop(p, None)
    export(GLOBAL, file_name)

GLOBAL = load('utils/config.json')
