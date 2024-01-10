from commands import GoBackCmd
from commands.EnterResultsCmd import EnterResultsCmd
from screens.base_screen import BaseScreen

class RoundResultsEntryView(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Entering results for {self.tournament.name}, Round {self.tournament.current_round}")
        for idx, match in enumerate(self.tournament.rounds[self.tournament.current_round - 1].matches, start=1):
            print(f"{idx}. {match.player1_id} vs {match.player2_id} - Enter '1' for player1 wins, '2' for player2 wins, 'T' for tie")

    def get_command(self):
        while True:
            choice = self.input_string("Enter match number and result (e.g., '1 1' for player1 wins in match 1), or type 'back' to return: ")
            if choice.lower() == 'back':
                return GoBackCmd()
            else:
                try:
                    match_number, result = choice.split()
                    match_index = int(match_number) - 1  # Adjust for 0-based index
                    if 0 <= match_index < len(self.tournament.rounds[self.tournament.current_round - 1].matches):
                        winner_id = self.determine_winner(match_index, result)
                        is_tie = result.lower() == 't'
                        print(f"Debug: Getting command for match index: {match_index}")  # New debug statement
                        return EnterResultsCmd(self.tournament, match_index, winner_id=winner_id, is_tie=is_tie)
                except ValueError:
                    print("Invalid input. Please try again.")

    def determine_winner(self, match_index, result):
        match = self.tournament.rounds[self.tournament.current_round - 1].matches[match_index]
        if result == '1':
            return match.player1_id
        elif result == '2':
            return match.player2_id
        return None
