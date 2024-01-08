from commands import RegisterPlayerCmd, EnterResultsCmd, AdvanceRoundCmd, GenerateReportCmd, GoBackCmd, NoopCmd
from screens.base_screen import BaseScreen

class TournamentView(BaseScreen):
    """Screen for viewing and managing a specific tournament."""

    def __init__(self, tournament, club_manager, players=None):
        self.tournament = tournament
        self.club_manager = club_manager
        self.players = players if players is not None else self.fetch_players()
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
                return NoopCmd("player-registration", tournament=self.tournament, players=self.players)
            elif choice == "2":
                return self.enter_results()
            elif choice == "3":
                return AdvanceRoundCmd(self.tournament)
            elif choice == "4":
                return GenerateReportCmd(self.tournament)
            elif choice == "5":
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")

    def fetch_players(self):
        return self.club_manager.fetch_all_players()

    def enter_results(self):
        if self.tournament.current_round is None or self.tournament.current_round > len(self.tournament.rounds):
            print("No current round available.")
            return GoBackCmd()

        current_round_matches = self.tournament.rounds[self.tournament.current_round - 1].matches
        for idx, match in enumerate(current_round_matches, 1):
            print(f"{idx}. Match ID: {match.id}, Players: {match.player1_id} vs {match.player2_id}")

        match_choice = self.input_string("Enter match number: ")
        if match_choice.isdigit():
            match_choice = int(match_choice) - 1
            if 0 <= match_choice < len(current_round_matches):
                match = current_round_matches[match_choice]
                result_choice = self.input_string("Enter result (1: Win, 2: Loss, 3: Tie): ")
                if result_choice == "1":
                    winner_id = self.input_string("Enter winner's player ID: ")
                    return EnterResultsCmd(self.tournament, match.id, winner_id=winner_id)
                elif result_choice == "2":
                    loser_id = self.input_string("Enter loser's player ID: ")
                    winner_id = match.player1_id if match.player2_id == loser_id else match.player2_id
                    return EnterResultsCmd(self.tournament, match.id, winner_id=winner_id)
                elif result_choice == "3":
                    return EnterResultsCmd(self.tournament, match.id, is_tie=True)
                else:
                    print("Invalid result choice.")
            else:
                print("Invalid match number.")
        else:
            print("Please enter a valid number.")

