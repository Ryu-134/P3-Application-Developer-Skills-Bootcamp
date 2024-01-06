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
            choice = self.input_string("Enter your choice: ")
            if choice.isdigit():
                choice = int(choice)
                if choice == 1:
                    return NoopCmd("tournament-list-view")
                elif choice == 2:
                    return NoopCmd("tournament-create")
                elif choice == 3:
                    return ExitCmd()
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid input. Please enter a number.")
