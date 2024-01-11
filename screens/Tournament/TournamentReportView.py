from commands.context import Context


class TournamentReportView:
    def __init__(self, tournament, next_cmd=None):
        self.tournament = tournament
        self.next_cmd = next_cmd

    def execute(self):
        # Calculate final points for players
        self.tournament.calculate_final_points()

        # Generate and print the tournament report
        print(f"Tournament Report for {self.tournament.name}")
        print(f"Dates: {self.tournament.start_date} - {self.tournament.end_date}")
        print("Players (sorted by points):")
        sorted_players = sorted(self.tournament.players, key=lambda p: self.tournament.player_points.get(p, 0),
                                reverse=True)
        for player in sorted_players:
            print(f"Player ID: {player}, Points: {self.tournament.player_points.get(player, 0)}")
        print("Rounds and Matches:")
        for idx, round in enumerate(self.tournament.rounds, start=1):
            print(f"Round {idx}")
            for match in round.matches:
                winner = 'Tie' if match.is_tie else match.winner_id
                print(f"  Match: Players: {match.player1_id} vs {match.player2_id}, Winner: {winner}")
        return Context(screen="main-menu")
