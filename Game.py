import random


class Game:

    def __init__(self, starting_player):
        if starting_player == 3:
            self.starting_player = random.randint(0,1)
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
        if self.is_done:
            return self.get_other_player()

