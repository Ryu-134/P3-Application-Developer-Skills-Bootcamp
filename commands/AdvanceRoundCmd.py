from commands.context import Context

class AdvanceRoundCmd:
    def __init__(self, tournament, club_manager, next_cmd=None):
        self.tournament = tournament
        self.club_manager = club_manager
        self.next_cmd = next_cmd

    def execute(self):
        # Logic to advance the tournament to the next round
        if self.tournament.can_advance_round():
            self.tournament.advance_to_next_round()
            print(f"Advanced to round {self.tournament.current_round} in {self.tournament.name}")
        else:
            print(f"Cannot advance round in {self.tournament.name}")

        # If there's a next_cmd, execute it
        if self.next_cmd:
            return self.next_cmd.execute()
        return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
