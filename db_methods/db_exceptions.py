# Define a custom exception class
class MaxPlayersReachedException(Exception):
    def __init__(self, message="The game has reached the maximum number of players"):
        self.message = message
        super().__init__(self.message)