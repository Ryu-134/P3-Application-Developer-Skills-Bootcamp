class UpdateMatchResultCmd:
    def __init__(self, tournament, match_number, result):
        self.tournament = tournament
        self.match_number = match_number - 1  # Adjusting for 0-based index
        self.result = result

    def execute(self):
        # Check if match_number is valid
        if 0 <= self.match_number < len(self.tournament.current_round.matches):
            match = self.tournament.current_round.matches[self.match_number]

            if self.result == '1':
                match.winner_id = match.player1_id
            elif self.result == '2':
                match.winner_id = match.player2_id
            elif self.result.lower() == 't':
                match.is_tie = True
            else:
                print("Invalid result entered.")
                return

            # Update player points
            self.tournament.update_points_after_round()
            print(f"Match result updated: {match}")
        else:
            print("Invalid match number.")
