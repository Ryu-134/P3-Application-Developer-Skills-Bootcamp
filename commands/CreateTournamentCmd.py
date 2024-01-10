from datetime import datetime
import sys
from models.tournament import Tournament
from commands.base import BaseCommand
from models.round import Round

class CreateTournamentCmd(BaseCommand):
    def __init__(self, name, venue, start_date, end_date, num_rounds, save_function):
        self.name = name
        self.venue = venue
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.num_rounds = num_rounds
        self.save_function = save_function

    def execute(self):
        # Initialize rounds as Round objects
        round_objects = [Round(matches=[]) for _ in range(self.num_rounds)]

        new_tournament = Tournament(
            name=self.name,
            venue=self.venue,
            start_date=self.start_date,
            end_date=self.end_date,
            players=[],
            rounds=round_objects,  # Use Round objects instead of dicts
            current_round=0
        )
        self.save_function(new_tournament)
        print(f"Tournament '{self.name}' created successfully.")
        sys.exit()