import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(os.path.abspath("models"))

from models.club_manager import ClubManager

def load_players_and_display(chess_id):
    data_folder_path = os.path.join(project_root, "data/clubs")

    # Initialize the ClubManager
    club_manager = ClubManager(data_folder=data_folder_path)

    # Search for the player across all clubs
    for club in club_manager.clubs:
        for player in club.players:
            if player.chess_id == chess_id:
                print(f"Player Found: {player.name}, Email: {player.email}, Birthday: {player.birthday}")
                return

    print("Player not found.")

if __name__ == "__main__":
    chess_id_input = input("Enter Chess ID: ")
    load_players_and_display(chess_id_input)
