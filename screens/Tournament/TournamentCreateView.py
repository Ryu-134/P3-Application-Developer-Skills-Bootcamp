from screens.base_screen import BaseScreen
from commands.CreateTournamentCmd import CreateTournamentCmd
from datetime import datetime
from commands.GoBackCmd import GoBackCmd


class TournamentCreateView(BaseScreen):
    def __init__(self, save_function):
        self.save_function = save_function

    def display(self):
        print("\nCreate a New Tournament")
        print("Please enter the following information:")

    def get_command(self):
        name = self.input_string("Enter the name of the tournament: ")
        venue = self.input_string("Enter the venue of the tournament: ")

        while True:
            start_date_str = self.input_string("Enter the start date (dd-mm-yyyy): ")
            end_date_str = self.input_string("Enter the end date (dd-mm-yyyy): ")

            try:
                # Parse the start and end dates
                start_date = datetime.strptime(start_date_str, '%d-%m-%Y')
                end_date = datetime.strptime(end_date_str, '%d-%m-%Y')

                # Check if the end date is before the start date
                if end_date < start_date:
                    print("End date cannot be earlier than start date. Please enter the dates again.")
                else:
                    break  # Valid dates
            except ValueError:
                print("Invalid date format. Please use dd-mm-yyyy format.")

        num_rounds = self.input_string("Enter the number of rounds: ")

        if not num_rounds.isdigit():
            print("Number of rounds must be a number. Please try again.")
            return GoBackCmd()

        return CreateTournamentCmd(name, venue, start_date_str, end_date_str, int(num_rounds), self.save_function)
