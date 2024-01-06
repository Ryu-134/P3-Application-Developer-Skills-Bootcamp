from commands import RegisterPlayerCmd, GoBackCmd
from screens.base_screen import BaseScreen

class PlayerRegistrationView(BaseScreen):
    """Screen for registering a player for a tournament."""

    def __init__(self, tournament, players, context):
        self.tournament = tournament
        self.players = players
        self.context = context

    def display(self):
        print(f"Register a player for the tournament: {self.tournament.name}")
        for idx, player in enumerate(self.players, 1):
            print(f"{idx}. {player.name} (Chess ID: {player.chess_id})")
        print("\nType a player number to register them.")
        print("Type 'search' to search for a player (by Chess ID or name).")
        print("Type 'back' to return to the previous screen.")

    def get_command(self):
        while True:
            choice = self.input_string("Enter your choice: ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(self.players):
                    selected_player = self.players[choice - 1]
                    # Pass the current context as an argument to RegisterPlayerCmd
                    return RegisterPlayerCmd(self.tournament, selected_player, self.context)
            elif choice.lower() == 'search':
                search_term = self.input_string("Enter Chess ID or player's name to search: ")
                return self.search_player(search_term)
            elif choice.lower() == 'back':
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")

    def search_player(self, search_term):
        search_term = search_term.lower()
        # Filter players based on the search term
        matching_players = [
            player for player in self.players
            if search_term in player.name.lower() or search_term in player.chess_id.lower()
        ]
        # Handle no matches
        if not matching_players:
            print("No players found matching the search term.")
            return GoBackCmd()
        # Display matching players
        print("\nMatching Players:")
        for idx, player in enumerate(matching_players, 1):
            print(f"{idx}. {player.name} (Chess ID: {player.chess_id})")
        # Allow user to select a player
        while True:
            choice = self.input_string("Select a player number to register, or type 'back': ")
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(matching_players):
                    selected_player = matching_players[choice - 1]
                    return RegisterPlayerCmd(self.tournament, selected_player)
            elif choice.lower() == 'back':
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")
