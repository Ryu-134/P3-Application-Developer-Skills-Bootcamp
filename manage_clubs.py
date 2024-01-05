from commands import ClubListCmd, NoopCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView
from models.club_manager import ClubManager
from models.tournament import Tournament
from screens.Tournament.TournamentListView import TournamentListView
from screens.Tournament.TournamentView import TournamentView
import json
import os
from pathlib import Path


#Verison 1.5

class App:
    """The main controller for the club management program"""

    SCREENS = {
        "main-menu": MainMenu,
        "club-create": ClubCreate,
        "club-view": ClubView,
        "player-view": PlayerView,
        "player-edit": PlayerEdit,
        "player-create": PlayerEdit,
        "tournament-list-view": TournamentListView,
        "tournament-view": TournamentView,
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
            tournaments.append(Tournament.load(str(tournament_file)))
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
            screen_class = self.SCREENS[self.context.screen]
            screen_args = {}

            # If the current screen is TournamentListView, pass the tournaments list
            if self.context.screen == "tournament-list-view" or screen_class == MainMenu:
                screen_args['tournaments'] = self.tournaments

            try:
                screen = screen_class(**screen_args)
                command = screen.run()
                self.context = command()
            except KeyboardInterrupt:
                print("Bye!")
                self.context.run = False

        for tournament in self.tournaments:
            self.save_tournament(tournament)


if __name__ == "__main__":
    app = App()
    app.run()
