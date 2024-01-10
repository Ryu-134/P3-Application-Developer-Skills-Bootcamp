from commands import ExitCmd
from commands.GoBackCmd import GoBackCmd
from commands.RefreshTournamentViewCmd import RefreshTournamentViewCmd
from commands.context import Context


class AdvanceRoundCmd:
    def __init__(self, tournament, club_manager, next_cmd=None):
        self.tournament = tournament
        self.club_manager = club_manager
        self.next_cmd = next_cmd

    def execute(self):
        # Check if all matches in the current round are completed and if it's not the last round
        if self.tournament.can_advance_round():
            self.tournament.advance_to_next_round()
            print(f"Advanced to round {self.tournament.current_round} in {self.tournament.name}")

            # Execute next_cmd if provided, to refresh the tournament view
            return self.next_cmd.execute() if self.next_cmd else Context(screen="tournament-view",
                                                                         tournament=self.tournament,
                                                                         club_manager=self.club_manager)

        # If the current round is the final round, and all matches are completed then
        elif self.tournament.current_round == self.tournament.total_rounds and all(
                match.completed for match in self.tournament.rounds[-1].matches):
            print("Tournament completed.")
            print("Options:")
            print("1. Go Back to Main Menu")
            print("2. Exit Application")
            choice = input("Enter your choice: ")
            if choice == "1":
                return GoBackCmd()
            elif choice == "2":
                return ExitCmd()
            else:
                print("Invalid choice. Returning to main menu.")
                return GoBackCmd()

        else:
            print(f"Cannot advance round in {self.tournament.name}")
            return RefreshTournamentViewCmd(self.tournament, self.club_manager)
