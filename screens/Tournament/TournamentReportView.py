from .base_screen import BaseScreen
from commands import GoBackCmd

class TournamentReportView(BaseScreen):
    """Screen for viewing a tournament report."""

    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"Tournament Report: {self.tournament.name}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print("\nPlayers (sorted by points):")
        sorted_players = sorted(self.tournament.players, key=lambda p: self.tournament.player_points.get(p.id, 0),
                         reverse=True)
        for player in sorted_players:
            print(f"{player.name} - Points: {self.tournament.player_points.get(player.id, 0)}")

        print("\nRounds and Matches:")
        for round_num, round in enumerate(self.tournament.rounds, start=1):
            print(f"Round {round_num}:")
            for match in round.matches:
                result = "Tie" if match.is_tie else f"Winner: {match.winner_id}"
                print(f"{match.player1_id} vs {match.player2_id} - {result}")
        print("\nType 'back' to return to the previous screen.")

    def get_command(self):
        choice = self.input_string()
        if choice.lower() == 'back':
            return GoBackCmd()
        else:
            print("Invalid command. Please type 'back' to return.")
            return None
