class AdvanceRoundCmd:
    def __init__(self, tournament):
        self.tournament = tournament

    def execute(self):
        # Logic to advance the tournament to the next round
        if self.tournament.can_advance_round():
            self.tournament.advance_to_next_round()
            print(f"Advanced to round {self.tournament.current_round_number} in {self.tournament.name}")
        else:
            print(f"Cannot advance round in {self.tournament.name}")
