from commands import UpdateMatchResultCmd, GoBackCmd
from screens.base_screen import BaseScreen

class RoundResultsEntryView(BaseScreen):
    """Screen for entering results of matches in the current round of a tournament."""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Entering results for {self.tournament.name}, Round {self.tournament.current_round}")
        for idx, match in enumerate(self.tournament.get_current_round_matches(), 1):
            print(f"{idx}. {match.player1} vs {match.player2} - Enter '1' for {match.player1} wins, '2' for {match.player2} wins, 'T' for tie")

    def get_command(self):
        while True:
            choice = self.input_string("Enter match number and result (e.g., '1 1' for player1 wins in match 1), or type 'back' to return: ")
            if choice.lower() == 'back':
                return GoBackCmd()
            else:
                try:
                    match_number, result = choice.split()
                    match_number = int(match_number)
                    if match_number in range(1, len(self.tournament.get_current_round_matches()) + 1):
                        return UpdateMatchResultCmd(self.tournament, match_number, result)
                except ValueError:
                    pass  # Invalid input format
                print("Invalid input. Please try again.")
