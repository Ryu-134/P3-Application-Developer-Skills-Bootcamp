import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(os.path.join(project_root, 'models'))

from models.tournament import Tournament

def load_tournament_and_display(file_name):
    file_path = os.path.join(project_root, "data", "clubs", file_name)

    # Load the tournament
    tournament = Tournament.load(file_path)

    # Display basic attributes of the tournament
    print(f"Tournament: {tournament.name}")
    print(f"Venue: {tournament.venue}")
    print(f"Start Date: {tournament.start_date}")
    print(f"End Date: {tournament.end_date}")

if __name__ == "__main__":
    tournament_file = input("Enter tournament file name: ")
    load_tournament_and_display(tournament_file)
