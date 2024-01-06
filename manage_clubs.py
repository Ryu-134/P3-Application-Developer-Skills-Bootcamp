from commands import ClubListCmd, NoopCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerEdit, PlayerView
from models.club_manager import ClubManager
from models.tournament import Tournament
from screens.Tournament.TournamentListView import TournamentListView
from screens.Tournament.TournamentView import TournamentView
from screens.Tournament.PlayerRegistrationView import PlayerRegistrationView
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
        "player-registration": PlayerRegistrationView,
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
        self.context = command.execute()
        while self.context.run:
            # Retrieve the correct screen class from the context
            screen_class = self.SCREENS.get(self.context.screen)
            if not screen_class:
                # Fallback to the main menu if the screen is not found or if returning from a previous screen
                if self.context.screen is None:
                    print("Returning to the main menu.")
                else:
                    print(f"No screen found for {self.context.screen}. Returning to the main menu.")
                self.context.screen = "main-menu"
                screen_class = self.SCREENS.get(self.context.screen)

            # Prepare arguments for the screen
            screen_args = self.context.kwargs

            # Pass specific arguments to certain screens if needed
            if screen_class == MainMenu:
                screen_args = {'tournaments': self.tournaments}
            elif screen_class == TournamentListView:
                screen_args = {'tournaments': self.tournaments}
            elif screen_class == TournamentView and 'selected_tournament' in self.context.kwargs:
                selected_tournament = self.context.kwargs['selected_tournament']
                screen_args = {'tournament': selected_tournament, 'club_manager': self.club_manager}
            elif screen_class == PlayerRegistrationView and 'tournament' in self.context.kwargs:
                all_players = self.club_manager.fetch_all_players()
                screen_args = {'tournament': self.context.kwargs['tournament'], 'players': all_players,
                               'context': self.context}


            # Instantiate and run the screen, and retrieve the next command
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
