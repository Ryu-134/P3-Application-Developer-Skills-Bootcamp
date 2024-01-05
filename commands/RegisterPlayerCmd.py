class RegisterPlayerCmd:
    def __init__(self, tournament, player_id):
        self.tournament = tournament
        self.player_id = player_id

    def execute(self):
        # Add player to the tournament if not already registered
        if self.player_id not in self.tournament.players:
            self.tournament.players.append(self.player_id)
            print(f"Player {self.player_id} registered in {self.tournament.name}")
        else:
            print(f"Player {self.player_id} is already registered in {self.tournament.name}")
