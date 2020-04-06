# -*- coding: utf-8 -*-
"""Module describing constants used in the project
"""

import os
import csv
import pprint

# Doodle csv file
TIME_SLOT_LINE = 5
GAME_START_LINE = TIME_SLOT_LINE + 1
DEFAULT_COURT_NUM = 5
PLAYER_NUM_PER_COURT = 4
DEFAULT_NTRP = 2.0

# Member csv file
MEMBER_START_LINE = 2

# PPrint
pp = pprint.PrettyPrinter(indent=4)

# Noisy names
noises = [u'마감합니다', 'Count']

def sanitize(players):
    for noise in noises:
        if noise in players:
            players.remove(noise)

    return players

def list_to_str(l, separator=" "):
    result = ""
    for i in xrange(len(l)-1):        
        result += l[i].encode('utf-8')+separator
    result += l[-1].encode('utf-8')
    return result

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]