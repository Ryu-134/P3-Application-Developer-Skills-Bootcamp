from commands.context import Context
from pathlib import Path

class EnterResultsCmd:
    def __init__(self, tournament, match_index, winner_id=None, is_tie=False, club_manager=None):
        self.tournament = tournament
        self.match_index = match_index
        self.winner_id = winner_id
        self.is_tie = is_tie
        self.club_manager = club_manager

    def execute(self):
        print(f"Debug: Executing EnterResultsCmd with match index: {self.match_index}")  # New debug statement
        current_round_matches = self.tournament.rounds[self.tournament.current_round - 1].matches
        print(f"Debug: Match index: {self.match_index}")  # Debug statement
        if 0 <= self.match_index < len(current_round_matches):
            match = current_round_matches[self.match_index]
            if self.is_tie:
                match.set_tie()
            elif self.winner_id:
                match.set_winner(self.winner_id)
            else:
                print("Invalid input for match result.")
                return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)

            # Update tournament points and save changes
            self.tournament.update_points_after_round()
            file_path = Path('data/tournaments') / f'{self.tournament.name}.json'
            self.tournament.save(file_path)

            print(f"Debug: Results updated for match at index {self.match_index}.")
            return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
        else:
            print(f"Match at index {self.match_index} not found in current round.")
            return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
