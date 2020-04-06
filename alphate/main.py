# -*- coding: utf-8 -*-
"""Module describing command line interface

Examples:
    $ athenad start -i 10.0.0.1

"""

# external library
import click
from datetime import date

# internal library
from init import initiate_database
from create import create_games
from analyze import analyze_games
from update import update_games
from export import export_games

@click.group()
def cli(**kwargs):
    pass

@cli.command()
@click.option('--input', '-i', type=str, default="members.csv",
              help='Indicate the location of the input file(the member csv file).')
@click.option('--output', '-o', type=str, default="members.json",
              help='Indicate the location of the output file (the member json file).')
def init(**kwargs):
    """Initialize member database
    """    
    initiate_database(**kwargs)    


@cli.command()
# @click.option('--input', '-i', type=str, default=date.today().isoformat()+"_doodle.csv",
#               help='Indicate the location of the input doodle csv file.')
@click.option('--members', '-m', type=str, default="members.json",
              help='Indicate the location of the member file.')
@click.option('--date', '-d', type=str, default=date.today().isoformat(),
              help='Indicate the game date.')
@click.option('--courts', '-c', type=str, default="",
              help='Indicate the court number for each time slot.')
@click.option('--court-shuffle', '-s', is_flag=True,
              help='Indicate whether to shuffle courts (if not, sorted order).')
@click.option('--threshold', '-t', type=float, default=1.0,
              help='Indicate threshold for fairness so that players do not attend games more than predefined threshold.')
@click.option('--verbose', '-v', is_flag=True,
              help='Whether or not to enable detailed verbose debug output.')
def create(**kwargs):
    """Create game based on doodle poll csv file
    """    
    create_games(**kwargs)


@cli.command()
@click.option('--date', '-d', type=str, default=date.today().isoformat(),
              help='Indicate the game date.')
@click.option('--members', '-m', type=str, default="members.json",
              help='Indicate the location of the member file.')
@click.option('--verbose', '-v', is_flag=True,
              help='Whether or not to enable detailed verbose debug output.')
def analyze(**kwargs):
    """Analyze the created games
    """    
    analyze_games(**kwargs)


@cli.command()
@click.option('--date', '-d', type=str, default=date.today().isoformat(),
              help='Indicate the game date.')
@click.option('--members', '-m', type=str, default="members.json",
              help='Indicate the location of the member file.')
def update(**kwargs):
    """Update members' fairness based on the latest game (fairness)
    """
    update_games(**kwargs)


@cli.command()
@click.option('--date', '-d', type=str, default=date.today().isoformat(),
              help='Indicate the game date.')
@click.option('--members', '-m', type=str, default="members.json",
              help='Indicate the location of the member file.')
def export(**kwargs):
    """Export the created games to the CSV file format
    """    
    export_games(**kwargs)

def run():
    cli()


# Test section
    
if __name__ == '__main__':
    run()
