# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""

import json
import codecs
from const import *

def update_games(**kwargs):
    game_date = kwargs['date']
    player_filename = game_date+"-player.json"
    member_filename = kwargs['members']

    # Get member info
    with open(member_filename, 'r') as f:
        members = json.load(f)

    # Get player info
    with open(player_filename, 'r') as f:
        players = json.load(f)

    for k, v in players.iteritems():
        try:
            members[k]['game'] += v['game']
            members[k]['apply'] += v['apply']
            members[k]['fairness'] = float(members[k]['game']) / members[k]['apply']
        except:
            print "%s does not exist in the member list." % (k)

    while True:
        yes_or_no = (raw_input("Do you want to update member DB based on today's game (y/n)? ")).lower()
        if yes_or_no in {"yes", "y"}:
            with codecs.open(member_filename, 'w', encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=4)        
            break
        elif yes_or_no in {"no", "n"}:
            break