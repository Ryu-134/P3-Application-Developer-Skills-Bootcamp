from datetime import datetime
from .round import Round
from .match import Match
import json

class Tournament:
    def __init__(self, name, venue, start_date, end_date, players=None, rounds=None, current_round=1):
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.players = players if players else []
        self.player_points = {player_id: 0 for player_id in self.players}
        self.current_round = current_round
        self.rounds = rounds if rounds else []

        for player_id in self.players:
            self.player_points[player_id] = 0

    def add_player(self, player_id):
        if player_id not in self.players:
            self.players.append(player_id)
            self.player_points[player_id] = 0

    def add_round(self, round_data):
        self.rounds.append(Round(**round_data))

    def update_points_after_round(self):
        # Iterate over the matches in the last round
        for match in self.rounds[-1].matches:
            if match.is_tie:
                # Both players get 0.5 points in a tie
                self.player_points[match.player1_id] += 0.5
                self.player_points[match.player2_id] += 0.5
            elif match.winner_id:
                # Winner gets 1 point, ensure winner_id is not None
                self.player_points[match.winner_id] += 1

    def to_json(self):
        return {
            "name": self.name,
            "venue": self.venue,
            "start_date": self.start_date.strftime('%Y-%m-%d'),
            "end_date": self.end_date.strftime('%Y-%m-%d'),
            "players": self.players,
            "rounds": [round.to_json() for round in self.rounds],
            "player_points": self.player_points,
            "current_round": self.current_round
        }

    def save(self, file_path):
        with open(file_path, 'w') as file:
            json.dump(self.to_json(), file, ensure_ascii=False, indent=4)

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

            start_date = datetime.strptime(data.get('dates', {}).get('from'),
                                           '%d-%m-%Y') if 'dates' in data and 'from' in data['dates'] else None
            end_date = datetime.strptime(data.get('dates', {}).get('to'), '%d-%m-%Y') if 'dates' in data and 'to' in \
                                                                                         data['dates'] else None

            rounds = []
            for round_data in data.get('rounds', []):
                matches = []
                for match_data in round_data:
                    match = Match(
                        player1_id=match_data['players'][0],
                        player2_id=match_data['players'][1],
                        winner_id=match_data.get('winner'),
                        is_tie=match_data.get('winner') is None and match_data.get('completed', False),
                        completed=match_data.get('completed', False)
                    )
                    matches.append(match)
                rounds.append(Round(matches=matches))

            return Tournament(
                name=data['name'],
                venue=data['venue'],
                start_date=start_date,
                end_date=end_date,
                players=data['players'],
                rounds=rounds,
                current_round=data.get('current_round', 1)
            )

    def calculate_final_points(self):
        # Reset points for all players before calculation
        for player_id in self.players:
            self.player_points[player_id] = 0

        # Calculate points for each match in every round
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if match.is_tie:
                    # Both players get 0.5 points in a tie
                    self.player_points[match.player1_id] += 0.5
                    self.player_points[match.player2_id] += 0.5
                elif match.winner_id is not None:
                    # Winner gets 1 point
                    self.player_points[match.winner_id] += 1

