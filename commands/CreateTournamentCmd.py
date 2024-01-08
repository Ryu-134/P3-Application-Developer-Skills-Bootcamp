from datetime import datetime
from models.tournament import Tournament
from commands.base import BaseCommand
from commands.noop import NoopCmd

class CreateTournamentCmd(BaseCommand):
    def __init__(self, name, venue, start_date, end_date, num_rounds, save_function):
        self.name = name
        self.venue = venue
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.num_rounds = num_rounds
        self.save_function = save_function

    def execute(self):
        new_tournament = Tournament(
            name=self.name,
            venue=self.venue,
            start_date=self.start_date,
            end_date=self.end_date,
            players=[],
            rounds=[{'matches': []} for _ in range(self.num_rounds)],
            current_round=1
        )
        self.save_function(new_tournament)
        print(f"Tournament '{self.name}' created successfully.")
        return NoopCmd("main-menu")
