from datetime import datetime
from models.round import Round
from models.match import Match
import json
import random

class Tournament:
    def __init__(self, name, venue, start_date, end_date, players=None, rounds=None, current_round=1, total_rounds=4):
        self.name = name
        self.venue = venue
        self.start_date = start_date
        self.end_date = end_date
        self.players = players if players else []
        self.player_points = {player_id: 0 for player_id in self.players}
        self.current_round = current_round
        self.rounds = rounds if rounds else []
        self.total_rounds = total_rounds


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
            "start_date": self.start_date.strftime('%d-%m-%Y'),
            "end_date": self.end_date.strftime('%d-%m-%Y'),
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

    def can_advance_round(self):
        # Check if all matches in the current round are completed
        all_matches_completed = all(match.completed for match in self.rounds[self.current_round - 1].matches)

        # Check if the current round is not the last one
        more_rounds_to_play = self.current_round < self.total_rounds

        return all_matches_completed and more_rounds_to_play

    def advance_to_next_round(self):
        print("Advancing to next round...")
        # Sort players by points in descending order
        sorted_players = sorted(self.players, key=lambda p: self.player_points[p], reverse=True)
        print(f"Sorted players by points: {sorted_players}")


        # Create new matches for the next round
        new_matches = []
        while len(sorted_players) >= 2:
            player1 = sorted_players.pop(0)
            potential_opponents = [p for p in sorted_players if not self.has_played_against(player1, p)]
            print(f"Potential opponents for {player1}: {potential_opponents}")


            if potential_opponents:
                opponent = random.choice(potential_opponents)
                sorted_players.remove(opponent)
                print(f"Selected opponent for {player1}: {opponent}")

            else:
                opponent = sorted_players.pop(0)
                print(f"No potential opponents left. Selected opponent for {player1}: {opponent}")


            new_matches.append(Match(player1_id=player1, player2_id=opponent))

        # Create and add the new round
        new_round = Round(matches=new_matches)
        self.rounds.append(new_round)
        self.current_round += 1
        print(f"New round added. Current round is now: {self.current_round}")


    def has_played_against(self, player1, player2):
        # Check if the players have already played against each other
        for round_obj in self.rounds:
            if any(match.player1_id == player1 and match.player2_id == player2 or
                   match.player1_id == player2 and match.player2_id == player1 for match in round_obj.matches):
                return True
        return False