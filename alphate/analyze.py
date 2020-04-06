# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""
import json
import numpy as np
from const import *

def analyze_games(**kwargs):    
    game_date = kwargs['date']
    game_filename = game_date+"-game.json"
    player_filename = game_date+"-player.json"
    member_filename = kwargs['members']
    verbose = kwargs['verbose']

    # Get member info
    with open(member_filename, 'r') as f:
        members = json.load(f)

    # Get game info
    with open(game_filename, 'r') as f:
        games = json.load(f)

    # Get player info
    with open(player_filename, 'r+') as f:
        players = json.load(f)    


    # Update player info based the current game
    for k, v in players.iteritems():
        player_game_num = 0
        for time, games_for_time in games.iteritems():
            player_game_num += sum(game.count(k) for game in games_for_time)
        v['game'] = player_game_num
        v['fairness'] = (float)(player_game_num) / v['apply']

    # First, check fairness
    fairness_dict = dict()
    fairness_list = []
    total_apply = 0
    total_game = 0
    for k, v in players.iteritems():
        fairness_list.append(v['fairness'])
        if v['fairness'] not in fairness_dict:
            fairness_dict[v['fairness']] = [k]
        else:
            fairness_dict[v['fairness']].append(k)            
        total_apply += v['apply']
        total_game += v['game']

    print "### FAIRNESS CHECKING ###"
    print "- Avg: %f, Max: %f, Min: %f" % ((float)(total_game)/total_apply, max(fairness_list), min(fairness_list))

    if verbose:
        print "[ FAIRNESS DISTRIBUTION ]"
        for k in sorted(fairness_dict.keys()):
            print "- %f: %s" % (k, list_to_str(fairness_dict[k]))
    
    print;
    # Second, check ntrp diff
    ntrp_diff_dict = dict()
    ntrp_diff_list = []
    for k, v in games.iteritems():
        for court_players in v:
            best_player = court_players[0]
            worst_player = court_players[1]
            ntrp_diff = float(members[best_player]['ntrp']) - float(members[worst_player]['ntrp'])
            ntrp_diff_list.append(ntrp_diff)         
            if ntrp_diff not in ntrp_diff_dict:
                ntrp_diff_dict[ntrp_diff] = [best_player+" "+worst_player+" at "+k]
            else:
                ntrp_diff_dict[ntrp_diff].append(best_player+" "+worst_player+" at "+k)
                
    print "### NTRP DIFFERENCE CHECKING ###"
    print "- Avg: %f, Max: %f, Min: %f" % (np.mean(ntrp_diff_list), max(ntrp_diff_list), min(ntrp_diff_list))
    if verbose:
        print "[ NTRP DIFF DISTRIBUTION ]"
        for k in sorted(ntrp_diff_dict.keys(), reverse=True):
            print "- %f:\n%s" % (k, list_to_str(ntrp_diff_dict[k], separator="\n"))  