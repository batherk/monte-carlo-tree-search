import re
from Ledge import Ledge
from NIM import NIM
from UCT_Tree import UCTTree
from copy import deepcopy
from ProgressBar import ProgressBar

# Constants
GAME_TYPES = ["NIM","Ledge"]


# Settings
USE_UI = True

GAME_TYPE = "NIM"
ROLLOUT_ITERATIONS = 1000
GAME_ITERATIONS = 50
STARTING_PLAYER_SIMULATIONS = 3
STARTING_PLAYER_ACTUAL = 1
EXPLORATION = 1

# NIM
STARTING_PIECES = 20
MAX_REMOVE = 7

# Ledge
BOARD = [1,0,1,2,0,1]

VERBOSE = True

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

    def __init__(self):
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
        if SIM:
            starting_player = self.starting_player_simulations
        else:
            starting_player = self.starting_player_actual

        if self.game_type =="NIM":
            return NIM(self.starting_pieces, self.max_remove, starting_player)
        elif self.game_type == "Ledge":
            return Ledge(deepcopy(self.board), starting_player)

    def sim_default(self, game):
        first_action = None
        while not game.is_done():
            action = self.tree.default_action(game)
            if not first_action:
                first_action = action
            game.perform_action(action)                
        return first_action

    def sim_tree(self,game):
        sequence = []
        while not game.is_done():
            state = game.get_state()
            if state not in self.tree:
                self.tree.add_state(game,state)
                sequence.append((state,None))
                return sequence
            action = self.tree.select_action(game)
            game.perform_action(action)
            sequence.append((state,action))
        return sequence[:-1]

    def backprop(self, state_action_sequence, result):
        for state, action in state_action_sequence:
            self.tree.update(state,action,result)

    def simulate_game(self,game):
        state_action_sequence = self.sim_tree(game)
        if not game.is_done():
            first_action = self.sim_default(game)
            state_action_sequence[len(state_action_sequence)-1] = (state_action_sequence[len(state_action_sequence)-1][0],first_action)
        self.backprop(state_action_sequence, game.get_end_result())
    
    def play_game(self,game):
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
        times = self.rollout_iterations
        for i in range(times):
            game = self.create_game()
            self.simulate_game(game)


    def evaluate_leaf(self,game:NIM, rollout_iterations=None):
        sum_results = 0

        if not rollout_iterations:
            rollout_iterations = self.rollout_iterations

        for i in range (rollout_iterations):
            game_copy = game.create_simulation_copy()
            while not game_copy.is_done():
                #print(game_copy.get_possible_actions())
                action = self.tree.default_action(game_copy)
                game_copy.perform_action(action)
            sum_results += game_copy.get_end_result()
        return sum_results/rollout_iterations          

    def play_games(self):
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
        print()
        
        print("How many times each player started:")
        print(f'Player 1: {player1_starts} ({player1_starts/self.game_iterations*100:.1f}%). Player 2: {self.game_iterations-player1_starts} ({(self.game_iterations-player1_starts)/self.game_iterations*100:.1f}%)\n')
        print("How many times each player won:")        
        print(f'Player 1: {player1_wins} ({player1_wins/self.game_iterations*100:.1f}%). Player 2: {self.game_iterations-player1_wins} ({(self.game_iterations-player1_wins)/self.game_iterations*100:.1f}%)')
        

gs = GameSimulatorUCT()
gs.play_games()