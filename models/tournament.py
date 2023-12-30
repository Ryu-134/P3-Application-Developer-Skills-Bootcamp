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
        self.player_points = {player_id: 0 for player_id in self.players}  # Initialize player points

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)
            self.player_points[player_id] = 0  # Initialize points for new player

    def add_round(self, round_data):
        self.rounds.append(Round(**round_data))

    def update_points_after_round(self):
        # Ensure that this method is called after each round
        for match in self.rounds[-1].matches:  # Assuming the last round is the current round
            if match.is_tie:
                # Both players get 0.5 points in a tie
                self.player_points[match.player1_id] += 0.5
                self.player_points[match.player2_id] += 0.5
            else:
                # Winner gets 1 point
                self.player_points[match.winner_id] += 1

    def to_json(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date.strftime('%d-%m-%Y'),
            "end_date": self.end_date.strftime('%d-%m-%Y'),
            "players": self.players,
            "rounds": [round.to_json() for round in self.rounds],
            "player_points": self.player_points  # Include player points in the JSON representation
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
            tournament = Tournament(**data)
            tournament.player_points = {player_id: 0 for player_id in tournament.players}  # Initialize player points
            return tournament
