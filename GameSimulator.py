GAME_TYPES = ['NIM','Ledge']

def get_user_input(message, legal_values, set_type=str):
    user_input = set_type(input(message))
    while user_input not in legal_values:
        user_input = set_type(input(f'Legal values: {legal_values}: '))
    return user_input

class GameSimulator:

    def __init__(self, game_type, game_iterations, rollout_iterations,starting_player,verbose):
        self.game_type = game_type
        self.rollout_iterations = rollout_iterations
        self.game_iterations = game_iterations
        self.starting_player = starting_player

    def run():
        pass

    