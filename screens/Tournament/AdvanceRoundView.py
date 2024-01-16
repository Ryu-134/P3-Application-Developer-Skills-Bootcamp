from commands.RefreshTournamentViewCmd import RefreshTournamentViewCmd
from commands.context import Context


class AdvanceRoundView:
    def __init__(self, tournament, club_manager, next_cmd=None):
        self.tournament = tournament
        self.club_manager = club_manager
        self.next_cmd = next_cmd

    def execute(self):
        confirmation = input("Are you sure you want to advance to the next round? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Advancing to the next round cancelled.")
            return RefreshTournamentViewCmd(self.tournament, self.club_manager)

        print(f"Checking if current round is final - Current Round: {self.tournament.current_round}"
              f", Total Rounds: {self.tournament.total_rounds}")
        print(f"Checking if all matches in the last round are completed.")

        # Check if the current round is the final round and all matches are completed
        if self.tournament.current_round == self.tournament.total_rounds and all(
                match.completed for match in self.tournament.rounds[-1].matches):
            print("Tournament completed. Exiting application.")
            exit(0)  # Exit the application

        # If it's not the final round, advance to the next round and generate new pairings
        elif self.tournament.can_advance_round():
            self.tournament.advance_to_next_round()
            print(f"Advanced to round {self.tournament.current_round} in {self.tournament.name}")

            # Print the state of new matches
            for match in self.tournament.rounds[-1].matches:
                print(f"New match - {match.player1_id} vs {match.player2_id}, Completed: {match.completed}")

            # Execute next_cmd if provided, to refresh the tournament view
            return self.next_cmd.execute() if self.next_cmd else Context(screen="tournament-view",
                                                                         tournament=self.tournament,
                                                                         club_manager=self.club_manager)
        else:
            print(f"Cannot advance round in {self.tournament.name}")
            return RefreshTournamentViewCmd(self.tournament, self.club_manager)
