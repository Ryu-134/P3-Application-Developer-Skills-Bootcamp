from .match import Match

class Round:
    def __init__(self, matches=None):
        self.matches = [Match(**match_data) for match_data in matches] if matches else []

    def add_match(self, match_data):
        self.matches.append(Match(**match_data))

    def to_json(self):
        return [match.to_json() for match in self.matches]
