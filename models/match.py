class Match:
    def __init__(self, player1_id, player2_id, winner_id=None, is_tie=False, completed=False):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner_id = winner_id
        self.is_tie = is_tie
        self.completed = completed

    def set_winner(self, winner_id):
        if self.is_tie:
            raise ValueError("Match has ended in a tie.")
        self.winner_id = winner_id
        self.completed = True

    def set_tie(self):
        self.is_tie = True
        self.winner_id = None
        self.completed = True

    def to_json(self):
        return {
            "players": [self.player1_id, self.player2_id],
            "winner_id": self.winner_id if not self.is_tie else None,
            "is_tie": self.is_tie,
            "completed": self.completed
        }
