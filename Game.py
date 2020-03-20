import random


class Game:

    def __init__(self, starting_player):
        if starting_player == 3:
            self.starting_player = random.randint(1,2)
        elif starting_player in [1,2]:
            self.starting_player = starting_player
        else:
            raise RuntimeError(f'{player} is not a legal player config. Should be 1,2 or 3.')
        self.current_player = self.starting_player

    def switch_player(self):
        self.current_player = self.get_other_player()

    def get_other_player(self):
        if self.current_player == 1:
            return 2
        else: 
            return 1
            
    def get_winner(self):
        if self.is_done():
            return self.get_other_player()

    def get_end_result(self):
        winner = self.get_winner()
        if winner == 1:
            return 1
        elif winner == 2:
            return -1 
    
    def get_child_states(self):
            child_states = []
            for action in self.get_possible_actions():
                sim_game = self.create_simulation_copy()
                sim_game.perform_action(action)
                child_states.append(sim_game.get_state())
            return child_states



