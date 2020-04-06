# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""
import codecs
import json
from const import *

def initiate_database(**kwargs):
    members = dict() 
    input_filename = kwargs['input']
    output_filename = kwargs['output']

    with open(input_filename, "r") as f:
        reader = list(unicode_csv_reader(f))[MEMBER_START_LINE:]
        for line in reader:             
            name = line[1]
            members[name] = dict()
            members[name]['gender'] = line[3]
            members[name]['level'] = line[5]
            try:
                members[name]['ntrp'] = float(line[6])
            except:
                print "%s's NTRP is not given (Apply default NTRP %f)" % (name, DEFAULT_NTRP)
                members[name]['ntrp'] = DEFAULT_NTRP
            members[name]['apply'] = 0
            members[name]['game'] = 0
            members[name]['fairness'] = 0.0
    
    while True:
        yes_or_no = (raw_input("This command will delete your old DB. Please back it up first.\nDo you really want to initialize member DB (y/n)? ")).lower()
        if yes_or_no in {"yes", "y"}:
            with codecs.open(output_filename, "w", encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=4)
            break
        elif yes_or_no in {"no", "n"}:
            break
