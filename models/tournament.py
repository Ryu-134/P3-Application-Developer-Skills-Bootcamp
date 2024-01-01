from datetime import datetime
from .round import Round
from .match import Match
import json

class Tournament:
    def __init__(self, name, venue, start_date, end_date, players=None, rounds=None):
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.players = players if players else []
        self.player_points = {player_id: 0 for player_id in self.players}

        self.rounds = []
        if rounds:
            for round_data in rounds:
                round_matches = []
                for match_data in round_data:
                    # Extract player IDs and winner ID from match_data
                    player1_id = match_data['players'][0]
                    player2_id = match_data['players'][1]
                    winner_id = match_data.get('winner')

                    # Determine if the match is a tie
                    is_tie = winner_id is None

                    # Create a Match object
                    match = Match(player1_id=match_data['players'][0], player2_id=match_data['players'][1],
                                  winner_id=match_data.get('winner'), is_tie=match_data.get('winner') is None)
                    round_matches.append(match)

                self.rounds.append(Round(matches=round_matches))
        for player_id in self.players:
            self.player_points[player_id] = 0


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

            # Extracting start and end dates from the nested 'dates' dictionary
            dates = data.get('dates', {})
            start_date_str = dates.get('from')
            end_date_str = dates.get('to')

            data['start_date'] = datetime.strptime(start_date_str, '%d-%m-%Y') if start_date_str else None
            data['end_date'] = datetime.strptime(end_date_str, '%d-%m-%Y') if end_date_str else None

            # Initialize Tournament with the modified data
            tournament = Tournament(name=data.get('name'),
                                    venue=data.get('venue'),
                                    start_date=data['start_date'],
                                    end_date=data['end_date'],
                                    players=data.get('players'),
                                    rounds=data.get('rounds'))
            return tournament

    def calculate_final_points(self):
        # Reset points for all players
        for player_id in self.players:
            self.player_points[player_id] = 0

        # Calculate points for each match in each round
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if match.is_tie:
                    # Both players get 0.5 points in a tie
                    self.player_points[match.player1_id] += 0.5
                    self.player_points[match.player2_id] += 0.5
                else:
                    # Winner gets 1 point
                    self.player_points[match.winner_id] += 1