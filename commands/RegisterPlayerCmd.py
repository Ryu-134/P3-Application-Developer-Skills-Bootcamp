class RegisterPlayerCmd:
    def __init__(self, tournament, player, context):
        self.tournament = tournament
        self.player = player
        self.context = context

    def execute(self):
        player_id = self.player.chess_id
        if player_id not in self.tournament.players:
            self.tournament.players.append(player_id)
            # Initialize player points to 0 if not already present
            self.tournament.player_points[player_id] = 0
            print(f"Player {self.player.name} (ID: {player_id}) registered in {self.tournament.name}")
        else:
            print(f"Player {self.player.name} (ID: {player_id}) is already registered in {self.tournament.name}")
        return self.context
