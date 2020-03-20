from Game import Game, random


class NIM(Game):
    """ 
    Class that contains the logic for the Nim game.
    Is instantiated with a number of pieces and the max amount of pieces to remove each round.
    """

    def __init__(self,start_amount_pieces, max_amount_remove, starting_player=1):
        """Creates a NIM object."""
        super(NIM,self).__init__(starting_player)
        if max_amount_remove >= start_amount_pieces:
            raise RuntimeError(f'Max amount of pieces one can remove must be lower than the total amount of pieces')
        if start_amount_pieces >= 100:
            raise RuntimeError(f'Start amount of pieces must be less than 100')
        if max_amount_remove <= 1:
            raise RuntimeError(f'Max amount of pieces must be greater than 1')
        self.start_amount_pieces = start_amount_pieces
        self.current_amount_pieces = start_amount_pieces
        self.max_amount_remove = max_amount_remove
        self.last_action = None

    def __str__(self):
        """Returns a string that explains the game's current state."""
        if not self.last_action:
            return f"Start pile: {self.current_amount_pieces}. Player {self.current_player} will start."
        elif self.is_done():
            return f"Player {self.get_winner()} won"
        else:
            return f"Player {self.get_other_player()} selected {self.last_action} stones: Remaining stones = {self.current_amount_pieces}"

    def perform_action(self,action):
        """¨Updates the current state by performing the action."""
        if action in self.get_possible_actions():
            self.current_amount_pieces -= action
            self.switch_player()
            self.last_action = action
        elif self.is_done():
            print("Game is done")
        else: 
            print("Not a possible move")

    def get_possible_actions(self):
        """¨Returns a list of the possible actions to perform given the game's current state."""
        return [number for number in range(1,self.max_amount_remove+1) if self.current_amount_pieces - number >= 0]

    def is_done(self):
        """Returns if the game is won or not."""
        return self.current_amount_pieces==0
    
    def copy(self):
        """Returns a deep copy of itsself."""
        game = NIM(self.start_amount_pieces, self.max_amount_remove, self.current_player)
        game.current_amount_pieces = self.current_amount_pieces
        game.last_action = self.last_action
        return game

    def get_state(self):
        """Gets the current state of the game."""
        return self.current_amount_pieces, self.current_player
