from commands import AdvanceRoundCmd, GoBackCmd
from .base_screen import BaseScreen

class NextRoundConfirmationView(BaseScreen):
    """Screen for confirming to advance to the next round of a tournament."""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Tournament: {self.tournament.name}")
        print(f"Current Round: {self.tournament.current_round_number}")
        print("Are you sure you want to advance to the next round? (yes/no)")

    def get_command(self):
        choice = self.input_string().lower()
        if choice == 'yes':
            return AdvanceRoundCmd(self.tournament)
        elif choice == 'no':
            return GoBackCmd()
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            return None
