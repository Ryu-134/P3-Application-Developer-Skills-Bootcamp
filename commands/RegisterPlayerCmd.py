from pathlib import Path


class RegisterPlayerCmd:
    def __init__(self, tournament, player, context):
        self.tournament = tournament
        self.player = player
        self.context = context

    def execute(self):
        player_id = self.player.chess_id
        if player_id not in self.tournament.players:
            self.tournament.players.append(player_id)
            self.tournament.player_points[player_id] = 0
            print(f"Player {self.player.name} (ID: {player_id}) registered in {self.tournament.name}")

            # Save the tournament after registering the player
            file_path = Path('data/tournaments') / f'{self.tournament.name}.json'
            self.tournament.save(file_path)
        else:
            print(f"Player {self.player.name} (ID: {player_id}) is already registered in {self.tournament.name}")

        return self.context
