from commands import ClubListCmd
from screens import ClubCreate, ClubView, MainMenu, PlayerView
from screens.players.edit import PlayerEdit
from models.club_manager import ClubManager
from models.tournament import Tournament
from screens.Tournament.TournamentListView import TournamentListView
from screens.Tournament.TournamentView import TournamentView
from screens.Tournament.PlayerRegistrationView import PlayerRegistrationView
from screens.Tournament.TournamentCreateView import TournamentCreateView
from commands.context import Context
import json
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
        "tournament-create": TournamentCreateView,
        "exit": False,
    }

    def __init__(self):
        self.club_manager = ClubManager()
        self.tournaments = self.load_tournaments()
        self.create_tournament_view = None

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
        self.create_tournament_view = TournamentCreateView(self.save_tournament)
        create_tournament_command = self.create_tournament_view.get_command()
        create_tournament_command.execute()

    def run(self):
        command = ClubListCmd()
        self.context = command.execute()

        while self.context.run:
            screen_class = self.SCREENS.get(self.context.screen)

            if not screen_class:
                if self.context.screen is None:
                    print("Returning to the main menu.")
                    self.context.screen = "main-menu"
                else:
                    print(f"No screen found for {self.context.screen}. Returning to the main menu.")
                self.context.screen = "main-menu"
                continue  # Ensure the loop continues after updating the context

            screen_args = self.context.kwargs

            if screen_class == MainMenu:
                screen_args = {'tournaments': self.tournaments}
            elif screen_class == TournamentListView:
                screen_args = {'tournaments': self.tournaments}
            elif screen_class == TournamentView and 'selected_tournament' in self.context.kwargs:
                selected_tournament = self.context.kwargs['selected_tournament']
                screen_args = {'tournament': selected_tournament, 'club_manager': self.club_manager}
            elif screen_class == PlayerRegistrationView:
                tournament = self.context.kwargs.get('tournament')
                if tournament:
                    all_players = self.club_manager.fetch_all_players()
                    # Pass the current context as an argument
                    screen_args = {
                        'tournament': tournament,
                        'players': all_players,
                        'context': self.context
                    }
            try:
                screen = screen_class(**screen_args)
                command = screen.run()

                # Check if the command is executable
                if hasattr(command, "execute"):
                    new_context = command.execute()

                    # Check if new_context is a Context instance
                    if isinstance(new_context, Context):
                        self.context = new_context
                        if self.context.screen == "tournament-view" and hasattr(self.context, 'tournament'):
                            # Reconstruct the tournament view with the updated context
                            screen_args = {'tournament': self.context.tournament, 'club_manager': self.club_manager}
                            TournamentView(**screen_args)
                            continue  # Continue the loop to refresh the screen
                    else:
                        print(f"Command execution did not return a Context object: {type(new_context).__name__}")
                        break
                else:
                    print("No command received.")
                    break

            except KeyboardInterrupt:
                print("Exiting the application. Bye!")
                break


if __name__ == "__main__":
    app = App()
    app.run()
