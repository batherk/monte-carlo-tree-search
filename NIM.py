from Game import Game, random


class NIM(Game):

    def __init__(self,start_amount_pieces, max_amount_remove, starting_player=1):
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

    def __str__(self):
        return f'NIM - Remaining: {self.current_amount_pieces}. Player: {self.current_player}. Max: {self.max_amount_remove}.'

    def perform_action(self,action):
        if action in self.get_possible_actions():
            self.current_amount_pieces -= action
            self.switch_player()
        elif self.is_done():
            print("Game is done")
        else: 
            print("Not a possible move")

    def get_possible_actions(self):
        return [number for number in range(1,self.max_amount_remove+1) if self.current_amount_pieces - number >= 0]

    def is_done(self):
        return self.current_amount_pieces==0
