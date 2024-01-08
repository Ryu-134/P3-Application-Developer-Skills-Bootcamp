class EnterResultsCmd:
    def __init__(self, tournament, match_id, winner_id=None, is_tie=False):
        self.tournament = tournament
        self.match_id = match_id
        self.winner_id = winner_id
        self.is_tie = is_tie

    def execute(self):
        match_found = False
        for match in self.tournament.rounds[self.tournament.current_round - 1].matches:
            if match.id == self.match_id:
                match_found = True
                if self.is_tie:
                    match.set_tie()
                else:
                    match.set_winner(self.winner_id)

        if match_found:
            self.tournament.update_points_after_round()
            print(f"Results updated for match {self.match_id}.")
        else:
            print(f"Match {self.match_id} not found in current round.")

