from datetime import datetime
from .round import Round

class Tournament:
    def __init__(self, name, venue, start_date, end_date, players=None, rounds=None):
        self.name = name
        self.venue = venue
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.players = players if players else []
        self.rounds = [Round(**r) for r in rounds] if rounds else []

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)

    # ... Other necessary methods ...

    def to_json(self):
        # Convert the tournament data to a JSON-compatible dictionary
        return {
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date.strftime('%d-%m-%Y'),
            "end_date": self.end_date.strftime('%d-%m-%Y'),
            "players": self.players,
            "rounds": [round.to_json() for round in self.rounds]
        }
