from datetime import datetime
import sys
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from commands.base import BaseCommand
from pathlib import Path
import itertools

class CreateTournamentCmd(BaseCommand):
    def __init__(self, name, venue, start_date, end_date, num_rounds, player_ids):
        self.name = name
        self.venue = venue
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.num_rounds = num_rounds
        self.player_ids = player_ids

    def execute(self):
        # Generate initial matches for the first round
        initial_matches = []
        for player1_id, player2_id in itertools.combinations(self.player_ids, 2):
            match = Match(player1_id=player1_id, player2_id=player2_id, winner_id=None, is_tie=False, completed=False)
            initial_matches.append(match)

        round_objects = [Round(matches=initial_matches if i == 0 else [])
                         for i in range(self.num_rounds)]

        new_tournament = Tournament(
            name=self.name,
            venue=self.venue,
            start_date=self.start_date,
            end_date=self.end_date,
            players=self.player_ids,
            rounds=round_objects,
            current_round=1,
            total_rounds=self.num_rounds
        )
        file_path = Path('data/tournaments') / f'{self.name}.json'
        new_tournament.save(file_path)
        print(f"Tournament '{self.name}' created successfully.")
        sys.exit()
