from Game import Game, random
from copy import deepcopy

class Ledge(Game):
    """ 
    Class that contains the logic for the Ledge game.
    Is instantiated with a board (list) of coppers(1), gold (2) and empty spaces (0). 
    """

    def __init__(self, board_init, starting_player=1):
        """Creates a Ledge object."""
        super(Ledge,self).__init__(starting_player)
        for value in board_init:
            if value not in [0,1,2]:
                raise RuntimeError('Board should only contain 0,1 or 2.')
        if board_init.count(2) != 1:
            raise RuntimeError('The board should have one Gold coin (2)')
        self.board = board_init
        self.last_action = None
        self.stones = {1:"copper", 2: "gold"}

    def __str__(self):
        """Returns a string that explains the game's current state."""
        if not self.last_action:
            return f"Start board: {self.board}. Player {self.current_player} will start."
        elif self.is_done():
            return f"{self.board}. {self.explenation_last_action()} and won."
        else:
            return f"{self.board}. {self.explenation_last_action()}."

    def explenation_last_action(self):
        """Returns a string with an explanation of what the last action was."""
        place_from, place_to = self.last_action
        if place_to == place_from and self.is_done():
            return f"Player {self.get_other_player()} picked up gold"
        elif place_to == place_from:
            return f"Player {self.get_other_player()} picked up copper"
        else:
            stone = self.stones[self.board[place_to]]
            return f"Player {self.get_other_player()} moved {stone} from {place_from} to {place_to}"
 
    def get_possible_actions(self):
        """¨Returns a list of the possible actions to perform given the game's current state."""
        if self.is_done():
            return []

        possible_actions = []
        last_open = 0
        for i,value in enumerate(self.board):
            if i == 0 and value:
                possible_actions.append((0,0))
                last_open = 1
            else: 
                if value:
                    for j in range(last_open,i):
                        possible_actions.append((i,j))
                    last_open = i+1
        return possible_actions

    def perform_action(self, action):
        """¨Updates the current state by performing the action."""
        if self.is_done():
            print('Game is done')
        elif action in self.get_possible_actions():
            if action == (0,0):
                self.board[0] = 0
            else:
                piece = self.board[action[0]]
                self.board[action[0]] = 0
                self.board[action[1]] = piece
            self.switch_player()
            self.last_action = action
        else: 
            print('Not a possible action')

    def is_done(self):
        """Returns if the game is won or not."""

        return self.board.count(2) == 0

    def copy(self):
        """Returns a deep copy of itsself."""
        copy = Ledge(deepcopy(self.board), self.current_player)
        copy.last_action = self.last_action
        return copy

    def get_state(self):
        """Gets the current state of the game."""
        return (tuple(self.board), self.current_player)
        