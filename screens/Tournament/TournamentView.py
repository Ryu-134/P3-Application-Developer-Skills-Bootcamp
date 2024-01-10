from commands import EnterResultsCmd, AdvanceRoundCmd, GenerateReportCmd, GoBackCmd, NoopCmd
from commands.RefreshTournamentViewCmd import RefreshTournamentViewCmd
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
                return AdvanceRoundCmd(self.tournament, self.club_manager)
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
            return self.refresh_tournament_view()

        current_round_matches = self.tournament.rounds[self.tournament.current_round - 1].matches
        ongoing_matches = [match for match in current_round_matches if not match.completed]

        if not ongoing_matches:
            print("All matches in the current round are completed.")
            return self.refresh_tournament_view()

        for idx, match in enumerate(ongoing_matches, 1):
            print(f"{idx}. Players: {match.player1_id} vs {match.player2_id}")

        match_choice = self.input_string("Enter match number: ")
        if match_choice.isdigit():
            match_index = int(match_choice) - 1
            if 0 <= match_index < len(ongoing_matches):
                match = ongoing_matches[match_index]
                result_choice = self.input_string("Enter result (1: Win, 2: Loss, 3: Tie): ")
                if result_choice == "1":
                    winner_id = self.input_string("Enter winner's player ID: ")
                    return EnterResultsCmd(self.tournament, match_index, winner_id=winner_id, club_manager=self.club_manager)
                elif result_choice == "2":
                    loser_id = self.input_string("Enter loser's player ID: ")
                    winner_id = match.player1_id if match.player2_id == loser_id else match.player2_id
                    return EnterResultsCmd(self.tournament, match_index, winner_id=winner_id, club_manager=self.club_manager)
                elif result_choice == "3":
                    return EnterResultsCmd(self.tournament, match_index, is_tie=True, club_manager=self.club_manager)
                else:
                    print("Invalid result choice.")
            else:
                print("Invalid match number.")
        else:
            print("Please enter a valid number.")

    def refresh_tournament_view(self):
        # Returns a command to refresh the tournament view
        return RefreshTournamentViewCmd(self.tournament, self.club_manager)
