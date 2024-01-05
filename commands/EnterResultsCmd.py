class EnterResultsCmd:
    def __init__(self, tournament, match_id, winner_id=None, is_tie=False):
        self.tournament = tournament
        self.match_id = match_id
        self.winner_id = winner_id
        self.is_tie = is_tie

    def execute(self):
        # Find match by ID and enter results
        match = next((m for m in self.tournament.current_round.matches if m.id == self.match_id), None)
        if match:
            if self.is_tie:
                match.set_tie()
                print(f"Match {self.match_id} ended in a tie.")
            else:
                match.set_winner(self.winner_id)
                print(f"Match {self.match_id} winner set to {self.winner_id}.")
        else:
            print(f"Match {self.match_id} not found in current round.")
