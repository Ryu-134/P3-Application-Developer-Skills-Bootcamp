from commands.context import Context
class EnterResultsCmd:
    def __init__(self, tournament, match_index, winner_id=None, is_tie=False, club_manager=None):
        self.tournament = tournament
        self.match_index = match_index
        self.winner_id = winner_id
        self.is_tie = is_tie
        self.club_manager = club_manager

    def execute(self):
        current_round_matches = self.tournament.rounds[self.tournament.current_round - 1].matches
        if 0 <= self.match_index < len(current_round_matches):
            match = current_round_matches[self.match_index]
            if self.is_tie:
                match.set_tie()
            else:
                match.set_winner(self.winner_id)

            self.tournament.update_points_after_round()
            print(f"Results updated for match at index {self.match_index}.")

            # Return to the tournament view with updated tournament
            return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
        else:
            print(f"Match at index {self.match_index} not found in current round.")

            # Return to the tournament view with the same tournament
            return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)


