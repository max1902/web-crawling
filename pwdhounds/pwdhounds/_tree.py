
import sys
import os
import json
import logging

from copy import deepcopy
from jsonschema import validate
from jsonschema.exceptions import ValidationError

MY_FILE = "spiders/result.json"
URL_PATTERN = '^(http.+)$'


def _output():
    res = []
    
    with open(MY_FILE) as fstraem:
        categories_js_data = json.load(fstraem)
    
    while categories_js_data:

        for cc in categories_js_data:
            copied_c = deepcopy(cc)
            copied_c.update({'deeper': []})
            try:
                validate_res(copied_c)
            except ValidationError as e:
                logging.warning(
                    'ValidationError: %s;\nSchema rule violation: %s;\nObject "%s"\n\n',
                    e.message, json.dumps(copied_c), e.schema
                )

            if not cc['parent_id']:
                res.append(copied_c)
                categories_js_data.remove(cc)
                continue
            
            parent = build_departments_tree(res, cc['parent_id'])
            if not parent:
                continue

            parent['deeper'].append(copied_c)
            categories_js_data.remove(cc)
    
    sort_by_index(res)
    res = sorted(res, key=lambda x: x['index'])

    with open('Final.csv', 'w') as fstraem:
        json.dump(res, fstraem)

def sort_by_index(res):
    # sorts recursively
    for r in res:
        r['deeper'] = sorted(r['deeper'], key=lambda x: x['index'])
        sort_by_index(r['deeper'])

def build_departments_tree(cats, parent_id):
    for cc in cats:
        if cc['id'] == parent_id:
            return cc
        p = build_departments_tree(cc['deeper'], parent_id)
        if p:
            return p

def validate_res(res, recursive=False):
    test = res if isinstance(res, list) else [res]
    for r in test:
        validate(r, common_schema)
        if recursive:
            validate_res(r['sub'], recursive)

common_schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string', 'minimum': 1},
        'parent_id': {'type': ['string', 'null']},
        'id': {'type': 'string', 'minimum': 1},
        'index': {'type': 'number'},
        'link': {
            'anyOf': [
                {'type': 'string', 'pattern': URL_PATTERN},
                {'type': 'null'}
            ],
        },
    },
    'required': ['name', 'id', 'link', 'parent_id', 'index']
}

if __name__ == '__main__':
    _output()