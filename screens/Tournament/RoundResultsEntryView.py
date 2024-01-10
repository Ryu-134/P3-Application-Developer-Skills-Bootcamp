from commands import GoBackCmd
from commands.EnterResultsCmd import EnterResultsCmd
from screens.base_screen import BaseScreen


class RoundResultsEntryView(BaseScreen):
    def __init__(self, tournament, club_manager):
        self.tournament = tournament
        self.club_manager = club_manager

    def display(self):
        print(f"Entering results for {self.tournament.name}, Round {self.tournament.current_round}")
        current_round_matches = self.tournament.rounds[self.tournament.current_round - 1].matches
        for idx, match in enumerate(current_round_matches, start=1):
            if not match.completed:
                print(f"{idx}. {match.player1_id} vs {match.player2_id} - Enter '1' for player1 wins, '2' for player2 wins, 'T' for tie")


    def get_command(self):
        while True:
            input_str = self.input_string("Enter match number and result, or type 'back' to return: ")
            if input_str.lower() == 'back':
                return GoBackCmd()
            else:
                try:
                    match_number_str, result_str = input_str.split()
                    match_index = int(match_number_str) - 1  # Convert to 0-based index
                    if 0 <= match_index < len(self.tournament.rounds[self.tournament.current_round - 1].matches):
                        winner_id = self.determine_winner(match_index, result_str)
                        is_tie = result_str.lower() == 't'
                        return EnterResultsCmd(self.tournament, match_index, winner_id=winner_id, is_tie=is_tie, club_manager=self.club_manager)
                    else:
                        print("Invalid match number. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter the match number and result separated by a space.")

    def determine_winner(self, match_index, result):
        match = self.tournament.rounds[self.tournament.current_round - 1].matches[match_index]
        if result == '1':
            return match.player1_id
        elif result == '2':
            return match.player2_id
        return None
