class GoBackCmd:
    def __init__(self, previous_screen=None):
        self.previous_screen = previous_screen

    def __call__(self, *args, **kwargs):
        return self.previous_screen
