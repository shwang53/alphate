# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""
import json
import codecs
import numpy as np
import operator
from const import *

def create_games(**kwargs):
    # input_filename = kwargs['input']
    game_date = kwargs['date']
    input_filename = game_date+"_doodle.csv"
    game_output_filename = game_date+"-game.json"
    player_output_filename = game_date+"-player.json"
    member_filename = kwargs['members']
    courts = kwargs['courts']
    court_shuffle = kwargs['court_shuffle']
    threshold = kwargs['threshold']
    is_new_player = False

    with open(input_filename, 'rU') as f:        
        # Read the input file
        reader = list(unicode_csv_reader(f))

    # Get time slot info
    time_slots = [time for time in reader[TIME_SLOT_LINE] if time]    
    courts = eval(courts) if courts else [DEFAULT_COURT_NUM for _ in time_slots]

    # Get member info
    with open(member_filename, 'r') as f:
        members = json.load(f)

    # Get today's players info
    players = dict()
    candidate_players = dict()
    for line in reader[GAME_START_LINE:]:
        name = line[0]
        apply_num = line.count("OK")

        if (name in noises) or (apply_num==0):
            continue

        players[name] = dict()
        if name in members:    
            try:    
                players[name]['ntrp'] = float(members[name]['ntrp'])
            except:
                print name
        else:
            is_new_player = True
            print name+"'s NTRP is not recorded."
            manual_ntrp = raw_input("Please enter his/her NTRP (float): ")
            players[name]['ntrp'] = float(manual_ntrp)
            # players[name]['ntrp'] = GUEST_DEFAULT_NTRP
            # Update new member
            members[name] = dict()
            members[name]['level'] = ""
            members[name]['gender'] = ""
            members[name]['ntrp'] = players[name]['ntrp']
            members[name]['game'] = 0
            members[name]['apply'] = 0
            members[name]['fairness'] = 0.0

        players[name]['apply'] = apply_num
        players[name]['game'] = 0
        players[name]['fairness'] = 0.0

        for i in xrange(len(time_slots)):
            if line[i+1] == 'OK':
                if i in candidate_players:
                    candidate_players[i].append(name)
                else:
                    candidate_players[i] = [name]

    unsorted_timeslot = list()
    for k, v in candidate_players.iteritems():
        unsorted_timeslot.append((k, len(v)))

    sorted_timeslot, _ = zip(*sorted(unsorted_timeslot, key=lambda x: x[1]))
    # print sorted_timeslot

    # Select players per each time slot.
    players_per_ts = dict()
    # for i in xrange(len(time_slots)):            
    for i in sorted_timeslot:
        sorted_players = [(player, players[player]['fairness'], members[player]['fairness'], -1*players[player]['ntrp']) for player in candidate_players[i]]
        # sorted_players = [(k, v['fairness'], members[k]['fairness'], -1*v['ntrp']) for k, v in players.iteritems()]
        sorted_players = sorted(sorted_players, key=lambda x: (x[1], x[2], x[3]))

        idx = 0
        for name, _ , _, _ in sorted_players:
            expected_fairness = float(players[name]['game']+1) / players[name]['apply']        
            if expected_fairness > threshold:
                break
            else:
                idx += 1

        required_player_num = courts[i] * PLAYER_NUM_PER_COURT if idx > courts[i] * PLAYER_NUM_PER_COURT else idx-idx%PLAYER_NUM_PER_COURT
        # required_player_num = courts[i] * PLAYER_NUM_PER_COURT if idx > courts[i] * PLAYER_NUM_PER_COURT else idx+(PLAYER_NUM_PER_COURT-idx%PLAYER_NUM_PER_COURT)
        # print required_player_num
        if required_player_num == 0:
            continue
        sorted_selected_players = sorted(sorted_players[:required_player_num], key=lambda x: x[3])
        selected_player_names, _, _, _ = zip(*sorted_selected_players)
                
        for name in selected_player_names:            
            players[name]['game'] += 1
            players[name]['fairness'] = float(players[name]['game']) / players[name]['apply']        

        players_for_courts = [selected_player_names[j:j+PLAYER_NUM_PER_COURT] for j in range(0, len(selected_player_names), PLAYER_NUM_PER_COURT)]
        reordered_players_for_courts = []

        for court_players in players_for_courts:
            court_players = list(court_players)
            ntrp_list = [players[name]['ntrp'] for name in court_players]            
            if np.min(ntrp_list) == np.max(ntrp_list):                
                np.random.shuffle(court_players)
            else:
                try:                
                    court_players[1], court_players[3] = court_players[3], court_players[1]
                    court_players[2], court_players[3] = court_players[3], court_players[2]
                except:
                    print court_players
            reordered_players_for_courts.append(court_players)

        if court_shuffle:
            np.random.shuffle(reordered_players_for_courts) 

        players_per_ts[time_slots[i]] = reordered_players_for_courts

    with codecs.open(game_output_filename, 'w', encoding='utf-8') as f:
        json.dump(players_per_ts, f, ensure_ascii=False, indent=4)

    with codecs.open(player_output_filename, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=4)

    while is_new_player:
        yes_or_no = (raw_input("Do you want to store new player's info into member DB (y/n)? ")).lower()
        if yes_or_no in {"yes", "y"}:
            with codecs.open(member_filename, 'w', encoding='utf-8') as f:
                json.dump(members, f, ensure_ascii=False, indent=4)        
            is_new_player = False
        elif yes_or_no in {"no", "n"}:
            break