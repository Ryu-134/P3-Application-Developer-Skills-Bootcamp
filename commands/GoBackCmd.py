from commands.context import Context


class GoBackCmd:
    def __init__(self, previous_screen=None):
        self.previous_screen = previous_screen

    def execute(self):
        return Context(screen=self.previous_screen)
