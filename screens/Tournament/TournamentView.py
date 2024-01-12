from commands import NoopCmd
from commands.RefreshTournamentViewCmd import RefreshTournamentViewCmd
from commands.GoBackCmd import GoBackCmd
from screens.Tournament.RoundResultsEntryView import RoundResultsEntryView
from screens.base_screen import BaseScreen
from screens.Tournament.AdvanceRoundView import AdvanceRoundView
from screens.Tournament.TournamentReportView import TournamentReportView


class TournamentView(BaseScreen):
    """Screen for viewing and managing a specific tournament."""

    def __init__(self, tournament, club_manager, players=None):
        self.tournament = tournament
        self.club_manager = club_manager
        if not self.club_manager:
            raise ValueError("Club manager cannot be None")
        self.players = players if players is not None else self.fetch_players()
        self.players = players if players is not None else self.fetch_players()

    def display(self):
        print(f"Tournament: {self.tournament.name}")
        print(f"Venue: {self.tournament.venue}")
        print(f"Start Date: {self.tournament.start_date}")
        print(f"End Date: {self.tournament.end_date}")
        print(f"Number of Rounds: {len(self.tournament.rounds)}")
        if self.tournament.current_round == 0:
            current_round_text = "Tournament hasn't started"
        elif self.tournament.current_round:
            current_round_text = f"Round {self.tournament.current_round}"
        else:
            current_round_text = "Tournament Ended"
        print(f"Current Round: {current_round_text}")
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
                # For registering a player, refresh the tournament view
                return NoopCmd("player-registration", tournament=self.tournament, players=self.players,
                               next_cmd=RefreshTournamentViewCmd(self.tournament, self.club_manager))
            elif choice == "2":
                # Enter results using RoundResultsEntryView
                command = self.enter_results()
                return command if command else RefreshTournamentViewCmd(self.tournament, self.club_manager)
            elif choice == "3":
                # After advancing to the next round, refresh the tournament view
                return AdvanceRoundView(self.tournament, self.club_manager,
                                       next_cmd=RefreshTournamentViewCmd(self.tournament, self.club_manager))
            elif choice == "4":
                # After generating a report, refresh the tournament view
                return TournamentReportView(self.tournament,
                                         next_cmd=RefreshTournamentViewCmd(self.tournament, self.club_manager))
            elif choice == "5":
                return GoBackCmd()
            else:
                print("Invalid choice. Please try again.")

    def enter_results(self):
        current_round_index = self.tournament.current_round - 1
        print(f"Debug: Current round index - {current_round_index}")  # Debug statement

        if current_round_index < len(self.tournament.rounds):
            current_round_matches = self.tournament.rounds[current_round_index].matches
            print(f"Debug: Number of matches in current round - {len(current_round_matches)}")  # Debug statement
            for i, match in enumerate(current_round_matches):
                print(f"Debug: Match {i + 1} status - {'completed' if match.completed else 'not completed'}")  # Debug statement
            for match in current_round_matches:
                print(f"Match between {match.player1_id} and {match.player2_id} completed: {match.completed}")
            if all(match.completed for match in current_round_matches):
                print("All matches in the current round are completed.")
                # Instead of refreshing the view, return a command to go back to the tournament options screen
                return RefreshTournamentViewCmd(self.tournament, self.club_manager)
            else:
                results_entry_view = RoundResultsEntryView(self.tournament, self.club_manager)
                results_entry_view.display()
                return results_entry_view.get_command()
        else:
            print("No current round available.")
            return RefreshTournamentViewCmd(self.tournament, self.club_manager)

    def fetch_players(self):
        return self.club_manager.fetch_all_players()

    def refresh_tournament_view(self):
        if self.club_manager:
            return self.club_manager.fetch_all_players()
        else:
            raise ValueError("Club manager is not set, cannot fetch players")
