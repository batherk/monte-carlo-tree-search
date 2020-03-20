import random
from abc import ABC, abstractclassmethod


class Game(ABC):
    """
    Abstract class for games.
    Is handling all the states, actions and rewards.
    """

    def __init__(self, starting_player):
        if starting_player == 3:
            self.starting_player = random.randint(1,2)
        elif starting_player in [1,2]:
            self.starting_player = starting_player
        else:
            raise RuntimeError(f'{player} is not a legal player config. Should be 1,2 or 3.')
        self.current_player = self.starting_player

    def switch_player(self):
        """Switches the current player to the other"""
        self.current_player = self.get_other_player()

    def get_other_player(self):
        """Returns the player that is not the current player"""
        if self.current_player == 1:
            return 2
        else: 
            return 1
            
    def get_winner(self):
        """Returns the winner of the game if it is finished. Else it returns None"""
        if self.is_done():
            return self.get_other_player()

    def get_end_result(self):
        """Returns the result of a won game"""
        winner = self.get_winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1 
    
    def get_child_states(self):
        """Returns a list of all possible child states from the given state"""
        child_states = []
        for action in self.get_possible_actions():
            sim_game = self.copy()
            sim_game.perform_action(action)
            child_states.append(sim_game.get_state())
        return child_states

    # Abstract methods

    @abstractclassmethod
    def is_done(self):
        """Returns if the game is won or not"""
        pass

    @abstractclassmethod
    def copy(self):
        """Returns a deep copy of itsself"""
        pass

    @abstractclassmethod
    def get_state(self):
        """Gets the current state of the game"""
        pass

    @abstractclassmethod
    def perform_action(self):
        """¨Updates the current state by performing the action."""
        pass

    @abstractclassmethod
    def get_possible_actions(self):
        """¨Returns a list of the possible actions to perform given the game's current state"""
        pass



