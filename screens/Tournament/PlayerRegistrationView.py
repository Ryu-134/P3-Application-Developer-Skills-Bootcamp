from commands import RegisterPlayerCmd, SearchPlayerCmd, GoBackCmd
from .base_screen import BaseScreen

class PlayerRegistrationView(BaseScreen):
    """Screen for registering a player for a tournament."""

    def __init__(self, tournament, players):
        self.tournament = tournament
        self.players = players  # This should be a list of all available players

    def display(self):
        print(f"Register a player for the tournament: {self.tournament.name}")
        for idx, player in enumerate(self.players, 1):
            print(f"{idx}. {player.name} (Chess ID: {player.chess_id})")
        print("Type 'search' to search for a player.")
        print("Type 'back' to go back to the tournament view.")

    def get_command(self):
        while True:
            choice = self.input_string("Enter a player number to register, 'search', or 'back': ")
            if choice.isdigit():
                choice = int(choice)
                if choice in range(1, len(self.players) + 1):
                    return RegisterPlayerCmd(self.tournament, self.players[choice - 1])
            elif choice.lower() == 'search':
                search_term = self.input_string("Enter Chess ID or player's name to search: ")
                return SearchPlayerCmd(search_term)
            elif choice.lower() == 'back':
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")
