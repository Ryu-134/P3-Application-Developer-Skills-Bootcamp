class GenerateReportCmd:
    def __init__(self, tournament, next_cmd=None):
        self.tournament = tournament
        self.next_cmd=next_cmd

    def execute(self):
        # Generate and print the tournament report
        print(f"Tournament Report for {self.tournament.name}")
        print(f"Dates: {self.tournament.start_date} - {self.tournament.end_date}")
        print("Players (sorted by points):")
        sorted_players = sorted(self.tournament.players, key=lambda p: self.tournament.player_points.get(p, 0), reverse=True)
        for player in sorted_players:
            print(f"Player ID: {player}, Points: {self.tournament.player_points.get(player, 0)}")
        print("Rounds and Matches:")
        for round in self.tournament.rounds:
            print(f"Round {round.number}")
            for match in round.matches:
                print(f"  Match: {match.id}, Players: {match.player1_id} vs {match.player2_id}, Winner: {match.winner_id if not match.is_tie else 'Tie'}")
