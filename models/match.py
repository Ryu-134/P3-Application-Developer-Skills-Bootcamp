class Match:
    def __init__(self, player1_id, player2_id, winner_id=None):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id

    def set_winner(self, winner_id):
        self.winner_id = winner_id

    def to_json(self):
        return {
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "winner_id": self.winner_id
        }
