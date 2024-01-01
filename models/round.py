class Round:
    def __init__(self, matches=None):
        if matches is None:
            self.matches = []
        else:
            # Assuming 'matches' is already a list of Match objects
            self.matches = matches

    def add_match(self, match):
        self.matches.append(match)

    def to_json(self):
        return [match.to_json() for match in self.matches]
