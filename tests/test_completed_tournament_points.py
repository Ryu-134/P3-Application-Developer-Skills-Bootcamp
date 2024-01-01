import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(project_root, 'models'))

from models.tournament import Tournament

file_path = os.path.join(project_root, "data", "tournaments", "completed.json")

tournament = Tournament.load(file_path)

# Ensure that calculate_final_points method is implemented in Tournament class
tournament.calculate_final_points()

for player_id, points in tournament.player_points.items():
    print(f"Player ID: {player_id}, Points: {points}")
