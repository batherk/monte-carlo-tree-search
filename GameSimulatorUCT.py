import re
from Ledge import Ledge
from NIM import NIM
from UCT_Tree import UCTTree
from copy import deepcopy
from ProgressBar import ProgressBar

# Constants
GAME_TYPES = ["NIM","Ledge"]


# Settings
USE_UI = False

GAME_TYPE = "NIM"
ROLLOUT_ITERATIONS = 1000
GAME_ITERATIONS = 30
STARTING_PLAYER_SIMULATIONS = 3
STARTING_PLAYER_ACTUAL = 1
EXPLORATION = 1

# NIM
STARTING_PIECES = 30
MAX_REMOVE = 4

# Ledge
BOARD = [1,0,1,2,0,1]

VERBOSE = False

# Help functions

def get_user_input(message, regex=None, legal_values=[], set_type=str):
    user_input = input(message)
    if regex:
        pattern = re.compile(regex)
        while not pattern.match(user_input):
            user_input = input(f'Regex: "{regex}": ')
    elif legal_values: 
        while user_input not in legal_values:
            user_input = input(f'Legal values: "{legal_values}": ')
    return set_type(user_input)
    

class GameSimulatorUCT:
    """
    A simulator class that uses UCT to learn and play games.
    """

    def __init__(self):
        """
        Creates a simulator object. 
        If USE_UI is True then the user can fill in the needed values.
        Else, the settings above the class definition is used.
        """
        if USE_UI:
            self.game_type = get_user_input("Game type: ",legal_values=GAME_TYPES)
            self.game_iterations = get_user_input("Game iterations: ", regex=r"[0-9]+",set_type=int)
            self.starting_player_actual = get_user_input("Starting player : ", regex=r"[1-3]", set_type=int)
            self.rollout_iterations = get_user_input("Rollout iterations: ", regex=r"[0-9]+",set_type=int)
            if self.game_type == "NIM":
                self.starting_pieces = get_user_input("Number of starting pieces: ", regex=r"[0-9]+",set_type=int)
                self.max_remove = get_user_input("Max allowed pieces to remove: ", regex=r"[0-9]+",set_type=int)
            else:
                self.board = []
                print("Add pieces to board: ")
                self.board.append(get_user_input("Add a piece: 0,1 or 2: ", regex=r"[0-2]", set_type=int))
                user_input = input("d - done adding pieces to board, c - continue: ")
                while user_input.upper() != "D":
                    if user_input.upper() == "C":
                        self.board.append(get_user_input("Add a piece: 0,1 or 2: ", regex=r"[0-2]", set_type=int))
                    user_input = input("d - done adding pieces to board, c - continue: ")
        else:
            self.game_type = GAME_TYPE
            self.rollout_iterations = ROLLOUT_ITERATIONS
            self.game_iterations = GAME_ITERATIONS
            self.starting_player_actual = STARTING_PLAYER_ACTUAL
            if self.game_type == "NIM":
                self.starting_pieces = STARTING_PIECES
                self.max_remove = MAX_REMOVE
            else:
                self.board = BOARD
        self.verbose = VERBOSE
        self.exploration = EXPLORATION
        self.tree = UCTTree(exploration=self.exploration)
        self.starting_player_simulations = STARTING_PLAYER_SIMULATIONS
        
    def create_game(self, SIM=True):
        """Creates a game based on the simulator's attributes."""
        if SIM:
            starting_player = self.starting_player_simulations
        else:
            starting_player = self.starting_player_actual

        if self.game_type =="NIM":
            return NIM(self.starting_pieces, self.max_remove, starting_player)
        elif self.game_type == "Ledge":
            return Ledge(deepcopy(self.board), starting_player)

    def sim_default(self, game):
        """Simulates a game by using the default policy. Returns the first action that is used for learning purposes."""
        first_action = None
        while not game.is_done():
            action = self.tree.default_action(game)
            if not first_action:
                first_action = action
            game.perform_action(action)                
        return first_action

    def sim_tree(self,game):
        """
        Simulates a game using the tree policy.
        It stops when the state is not recognized in the UCT-tree structure.
        Returns a list of state-action pairs that have been visited.
        """
        sequence = []
        while not game.is_done():
            state = game.get_state()
            if state not in self.tree:
                self.tree.add_state(game)
                return sequence
            action = self.tree.select_action(game)
            game.perform_action(action)
            sequence.append((state,action))
        return sequence

    def backprop(self, state_action_sequence, result):
        """Iterates through a list of state-action pairs and updates the UCT-values based on the end result."""
        for state, action in state_action_sequence:
            self.tree.update(state,action,result)

    def simulate_game(self,game):
        """Simulates a game and updates the UCT-tree with the results"""
        state_action_sequence = self.sim_tree(game)
        if not game.is_done():
            state = game.get_state()
            action = self.sim_default(game)
            state_action_sequence.append((state,action))
        self.backprop(state_action_sequence, game.get_end_result())
    
    def play_game(self,game):
        """
        Plays a game using preferably the tree policy, but if that's not possible, using the default policy.
        Prints the game's states if verbose is set to True.
        """
        if self.verbose:
            print(game)
        while not game.is_done():
            if game.get_state() in self.tree:
                action = self.tree.select_action(game)
            else:
                action = self.tree.default_action(game)
            game.perform_action(action)
            if self.verbose:
                print(game)

    def simulate_games(self):
        """Simulates games given the amount of rollout iterations."""
        times = self.rollout_iterations
        for i in range(times):
            game = self.create_game()
            self.simulate_game(game)

    def evaluate_leaf(self,game):
        """Returns the evaulation of a state by a rollout and using the default policy."""
        game_copy = game.copy()
        while not game_copy.is_done():
            action = self.tree.default_action(game_copy)
            game_copy.perform_action(action)
        return game_copy.get_end_result()
               
    def play_games(self):
        """
        Plays the amount of games that is given by game_iterations.
        If self.verbose is set to False, the progress of the games played will be shown.
        Lastly, the result statistics of the games played will be printed. 
        """
        player1_wins = 0
        player1_starts = 0
        if not self.verbose:
            progress = ProgressBar(self.game_iterations, "Playing games:")
        for i in range(self.game_iterations):
            self.tree = UCTTree(self.exploration)
            self.simulate_games()
    
            self.tree.exploration = 0
            game = self.create_game(SIM=False)

            if game.current_player == 1:
                player1_starts += 1
            if self.verbose:
                print(f"\nGame {i+1} of {self.game_iterations}:\n")
            self.play_game(game)

            if self.verbose:
                print()
            else: 
                progress.show(i)
            if game.get_winner() == 1:
                player1_wins += 1
        
        print(f'\nPlayer 1 started {player1_starts} of {self.game_iterations} games ({player1_starts/self.game_iterations*100:.1f}%).')        
        print(f'Player 1 won {player1_wins} of {self.game_iterations} games ({player1_wins/self.game_iterations*100:.1f}%).\n')
        

gs = GameSimulatorUCT()
gs.play_games()
