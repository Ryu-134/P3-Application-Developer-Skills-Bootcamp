from commands import ClubListCmd, NoopCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView
import json
import os
from pathlib import Path


class App:
    """The main controller for the club management program"""

    SCREENS = {
        "main-menu": MainMenu,
        "club-create": ClubCreate,
        "club-view": ClubView,
        "player-view": PlayerView,
        "player-edit": PlayerEdit,
        "player-create": PlayerEdit,
        "exit": False,
    }

    def __init__(self):
        # We start with the list of clubs (main menu)
        self.club_manager = ClubManager()
        self.tournaments = self.load_tournaments()

    def load_tournaments(self):
        tournaments = []
        tournaments_path = Path('data/tournaments')
        for tournament_file in tournaments_path.glob('*.json'):
            with open(tournament_file, 'r') as file:
                tournament_data = json.load(file)
                tournaments.append(Tournament.load(tournament_data))
        return tournaments

    def save_tournament(self, tournament):
        file_path = Path('data/tournaments') / f'{tournament.name}.json'
        with open(file_path, 'w') as file:
            json.dump(tournament.to_json(), file, indent=4)

    def create_tournament(self):
        # Add logic here to prompt the user for tournament details
        # Create a new Tournament instance.
        pass
    def run(self):
        command = ClubListCmd()
        self.context = command()

        while self.context.run:
            # Get the screen class from the mapping
            screen = self.SCREENS[self.context.screen]
            try:
                # Run the screen and get the command
                command = screen(**self.context.kwargs).run()
                # Run the command and get a context back
                self.context = command()
            except KeyboardInterrupt:
                # Ctrl-C
                print("Bye!")
                self.context.run = False
        # Save all tournaments when application exits
        for tournament in self.tournaments:
            self.save_tournament(tournament)


if __name__ == "__main__":
    app = App()
    app.run()
