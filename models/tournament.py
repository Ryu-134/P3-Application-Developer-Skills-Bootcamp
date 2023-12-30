# models/tournament.py

from datetime import datetime
from .round import Round
import json

class Tournament:
    def __init__(self, name, venue, start_date, end_date, players=None, rounds=None):
        self.name = name
        self.venue = venue
        self.start_date = datetime.strptime(start_date, '%d-%m-%Y')
        self.end_date = datetime.strptime(end_date, '%d-%m-%Y')
        self.players = players if players else []
        self.rounds = [Round(**round_data) for round_data in rounds] if rounds else []

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)

    def add_round(self, round_data):
        self.rounds.append(Round(**round_data))

    def to_json(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date.strftime('%d-%m-%Y'),
            "end_date": self.end_date.strftime('%d-%m-%Y'),
            "players": self.players,
            "rounds": [round.to_json() for round in self.rounds]
        }

    def save(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.to_json(), file, ensure_ascii=False, indent=4)

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            data['start_date'] = datetime.strptime(data['start_date'], '%d-%m-%Y')
            data['end_date'] = datetime.strptime(data['end_date'], '%d-%m-%Y')
            data['rounds'] = [Round(**round_data) for round_data in data['rounds']]
            return Tournament(**data)
