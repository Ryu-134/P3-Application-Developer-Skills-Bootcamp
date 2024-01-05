from commands import RegisterPlayerCmd, EnterResultsCmd, AdvanceRoundCmd, GenerateReportCmd, GoBackCmd
from screens.base_screen import BaseScreen

class TournamentView(BaseScreen):
    """Screen for viewing and managing a specific tournament."""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Tournament: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Start Date: {self.tournament.start_date}")
        print(f"End Date: {self.tournament.end_date}")
        print(f"Number of Rounds: {len(self.tournament.rounds)}")
        print(f"Current Round: {self.tournament.current_round or 'Tournament Ended'}")
        print("Players: ")
        for player_id in self.tournament.players:
            print(f"- Player ID: {player_id}")

        print("\nOptions:")
        print("1. Register a Player")
        print("2. Enter Results for Current Round")
        print("3. Advance to Next Round")
        print("4. Generate Tournament Report")
        print("5. Go Back to Main Menu")

    def get_command(self):
        while True:
            choice = self.input_string("Enter your choice: ")
            if choice == "1":
                return RegisterPlayerCmd(self.tournament)
            elif choice == "2":
                return EnterResultsCmd(self.tournament)
            elif choice == "3":
                return AdvanceRoundCmd(self.tournament)
            elif choice == "4":
                return GenerateReportCmd(self.tournament)
            elif choice == "5":
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")
