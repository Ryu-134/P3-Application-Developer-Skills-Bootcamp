from screens.base_screen import BaseScreen
from commands import NoopCmd, ExitCmd
from commands import GoBackCmd

class TournamentListView(BaseScreen):
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display(self):
        print("Available Tournaments:")
        for idx, tournament in enumerate(self.tournaments, start=1):
            print(f"{idx}. {tournament.name} - {tournament.venue}")

    def get_command(self):

        while True:
            choice = self.input_string("Select a tournament number or type 'exit' to go back: ")

            if choice.lower() == 'exit':
                return GoBackCmd()  # Assuming you have a command to go back

            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(self.tournaments):
                    # Return command to view the selected tournament
                    return NoopCmd("tournament-view", selected_tournament=self.tournaments[choice - 1])

            print("Invalid choice. Please try again.")
