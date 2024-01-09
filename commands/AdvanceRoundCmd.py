from commands.context import Context
class AdvanceRoundCmd:
    def __init__(self, tournament, club_manager):
        self.tournament = tournament
        self.club_manager = club_manager

    def execute(self):
        # Logic to advance the tournament to the next round
        if self.tournament.can_advance_round():
            self.tournament.advance_to_next_round()
            print(f"Advanced to round {self.tournament.current_round_number} in {self.tournament.name}")
        else:
            print(f"Cannot advance round in {self.tournament.name}")
        return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
