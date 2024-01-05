from commands import ClubListCmd, NoopCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView
from models.club_manager import ClubManager
from models.tournament import Tournament
from screens.Tournament.TournamentListView import TournamentListView
from screens.Tournament.TournamentView import TournamentView
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
        self.context = command.execute()  # or simply command() if your Command class is callable

        while self.context.run:
            # Retrieve the correct screen class from the context
            screen_class = self.SCREENS.get(self.context.screen)
            if not screen_class:
                print(f"No screen found for {self.context.screen}")
                break
            screen_args = self.context.kwargs

            if screen_class == MainMenu:
                # Pass tournaments to MainMenu
                screen_args['tournaments'] = self.tournaments
            elif screen_class == TournamentView and 'selected_tournament' in self.context.kwargs:
                screen_args['tournament'] = self.context.kwargs['selected_tournament']

            try:
                screen = screen_class(**screen_args)
                command = screen.run()
                self.context = command.execute()
            except KeyboardInterrupt:
                print("Exiting the application. Bye!")
                break


if __name__ == "__main__":
    app = App()
    app.run()
