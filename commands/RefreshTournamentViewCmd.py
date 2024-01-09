from commands.context import Context


class RefreshTournamentViewCmd:
    def __init__(self, tournament, club_manager):
        self.tournament = tournament
        self.club_manager = club_manager

    def execute(self):
        # Simply returns a context object to refresh the tournament view
        return Context(screen="tournament-view", tournament=self.tournament, club_manager=self.club_manager)
