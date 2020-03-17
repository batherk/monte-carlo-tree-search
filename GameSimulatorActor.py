import re
from Ledge import Ledge
from NIM import NIM
from Actor import RandomActor

# Constants
GAME_TYPES = ["NIM","Ledge"]


# Settings
USE_UI = False

GAME_TYPE = "Ledge"
ROLLOUT_ITERATIONS = 500
GAME_ITERATIONS = 1
STARTING_PLAYER = 1

# NIM
STARTING_PIECES = 20
MAX_REMOVE = 7

# Ledge
BOARD = [1,0,1,2,0,1]

VERBOSE = True

# Help functions

def convert_raises_exception(input,convertion):
    try:
        convertion(input)
        return True
    except ValueError:
        return False


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
    

class GameSimulatorActor:

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
        
    def create_one_game(self):
        if self.game_type =="NIM":
            return NIM(self.starting_pieces, self.max_remove, self.starting_player)
        elif self.game_type == "Ledge":
            return Ledge(self.board, self.starting_player)

    def run_one_rollout(self, game, actor1, actor2=None):
        while not game.is_done():
            actor = actor1
            if actor2 and game.current_player == 2:
                actor = actor2
            action = actor.get_action(game)
            game.perform_action(action)
        return game.get_end_result()

    def run_one_game(self,game, actor1, actor2=None):
        if self.verbose:
            print(game)
        while not game.is_done():
            actor = actor1
            if actor2 and game.current_player == 2:
                actor = actor2
            state = game.get_state()
            for i in range(self.rollout_iterations):
                simulation_copy = game.create_simulation_copy()
                action = actor.get_action(simulation_copy)
                simulation_copy.perform_action(action)

                end_result = self.run_one_rollout(simulation_copy, actor1, actor2)
                
                actor.update(state, action, end_result)

            action = actor.get_best_action(state)
            game.perform_action(action)
            if self.verbose:
                print(game)

    def run(self, actor1, actor2=None):
        for i in range(self.game_iterations):
            game = self.create_one_game()
            self.run_one_game(game,actor1,actor2)
        

gs = GameSimulatorActor()

actor1 = RandomActor()
actor2 = RandomActor(False)
gs.run(actor1, actor2)
    