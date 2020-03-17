import re
from Ledge import Ledge
from NIM import NIM
from UCT_Tree import UCTTree
from copy import deepcopy

# Constants
GAME_TYPES = ["NIM","Ledge"]


# Settings
USE_UI = False

GAME_TYPE = "Ledge"
ROLLOUT_ITERATIONS = 500
GAME_ITERATIONS = 50
STARTING_PLAYER = 1

# NIM
STARTING_PIECES = 20
MAX_REMOVE = 7

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

    def __init__(self):
        if USE_UI:
            self.game_type = get_user_input("Game type: ",legal_values=GAME_TYPES)
            self.game_iterations = get_user_input("Game iterations: ", regex=r"[0-9]+",set_type=int)
            self.starting_player = get_user_input("Starting player : ", regex=r"[1-3]", set_type=int)
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
            self.starting_player = STARTING_PLAYER
            if self.game_type == "NIM":
                self.starting_pieces = STARTING_PIECES
                self.max_remove = MAX_REMOVE
            else:
                self.board = BOARD
        self.verbose = VERBOSE
        self.tree = UCTTree()
        
    def create_game(self):
        if self.game_type =="NIM":
            return NIM(self.starting_pieces, self.max_remove, self.starting_player)
        elif self.game_type == "Ledge":
            return Ledge(deepcopy(self.board), self.starting_player)

    def simulate_default(self, game):
        first_action = None

        while not game.is_done():
            action = self.tree.default_action(game)

            if not first_action:
                first_action = action

            game.perform_action(action)
        return game.get_end_result(), first_action

    def simulate_tree(self,game):
        sequence = []
        if self.verbose:
            print(game)
        while not game.is_done():
            state = game.get_state()
            
            if state not in self.tree:
                self.tree.add_state(game,state)
                sequence.append((state,None))
                return sequence
            action = self.tree.select_action(game)
            game.perform_action(action)
            sequence.append((state,action))
            if self.verbose:
                print(game)
        return sequence[:-1]

    def backup(self, state_action_sequence, result):
        for state, action in state_action_sequence:
            self.tree.update(state,action,result)

    def simulate_one_game(self,game):
        state_action_sequence = self.simulate_tree(game)

        if game.is_done():
            self.backup(state_action_sequence,game.get_end_result())
        else:
            for i in range(self.rollout_iterations):
                rollout_game = game.create_simulation_copy()
                result, first_action = self.simulate_default(rollout_game)
                state_action_sequence[len(state_action_sequence)-1] = (state_action_sequence[len(state_action_sequence)-1][0],first_action)
                self.backup(state_action_sequence, result)

    def simulate_all_games(self):
        for i in range(self.game_iterations):
            #self.tree = UCTTree(exploration=1) # This creates a new tree for each simulation -> no inter game learning
            game = self.create_game()
            self.simulate_one_game(game)
        for state in self.tree.states:
            print(state)
            for action in self.tree.states[state]["A"]:
                print(action, self.tree.state_action_pairs[(state,action)])
            print()
            
        self.verbose = True
        game = self.create_game()
        self.simulate_one_game(game)

        

gs = GameSimulatorUCT()
gs.simulate_all_games()
    