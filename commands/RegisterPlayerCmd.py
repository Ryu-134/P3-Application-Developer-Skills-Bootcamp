class RegisterPlayerCmd:
    def __init__(self, tournament, player, context):
        self.tournament = tournament
        self.player = player
        self.context = context

    def execute(self):
        if self.player.chess_id not in self.tournament.players:
            self.tournament.players.append(self.player.chess_id)
            print(f"Player {self.player.name} (ID: {self.player.chess_id}) registered in {self.tournament.name}")
        else:
            print(f"Player {self.player.name} (ID: {self.player.chess_id}) is already registered in {self.tournament.name}")
        return self.context
