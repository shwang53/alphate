# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""

import json
from const import *
import pandas as pd

def export_games(**kwargs):
    game_date = kwargs['date']
    game_filename = game_date+"-game.json"
    output_filename = game_date+"-game.csv"

    # Get game info
    with open(game_filename, 'r') as f:
        games = json.load(f)

    table_list = list()
    for k in sorted(games.keys()):
        time_slot_A = list()
        time_slot_B = list()
        time_slot_A.append(k)
        time_slot_B.append(k)
        for court in games[k]:            
            # court_players = list_to_str(court, separator='\t')
            # time_slot.append(court_players)
            time_slot_A += court[:2]
            time_slot_B += court[2:]
        table_list.append(time_slot_A)
        table_list.append(time_slot_B)
    
    df = pd.DataFrame.from_records(table_list)    
    df.to_csv(output_filename, sep='\t', encoding='utf-8', index=False)