from commands import ExitCmd, NoopCmd
from screens.base_screen import BaseScreen

class MainMenu(BaseScreen):
    """Main menu screen"""

    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display(self):
        print("Main Menu")
        print("1. View Tournaments")
        print("2. Create New Tournament")
        print("3. Exit")

    def get_command(self):
        while True:
            value = self.input_string("Enter your choice: ")
            if value.isdigit():
                value = int(value)
                if value == 1:
                    return NoopCmd("tournament-list-view")
                elif value == 2:
                    return NoopCmd("tournament-create")
            elif value.upper() == "X":
                return ExitCmd()
            else:
                print("Invalid choice. Please try again.")
