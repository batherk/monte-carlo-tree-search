from Game import Game, random
from copy import deepcopy

class Ledge(Game):

    def __init__(self, board_init, starting_player=1):
        super(Ledge,self).__init__(starting_player)
        for value in board_init:
            if value not in [0,1,2]:
                raise RuntimeError('Board should only contain 0,1 or 2.')
        if board_init.count(2) != 1:
            raise RuntimeError('The board should have one Gold coin (2)')
        self.board = board_init

    def __str__(self):
        return f'Ledge - Board: {self.board}. Player: {self.current_player}.'

    def get_possible_actions(self):
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
        else: 
            print('Not a possible action')

    def is_done(self):
        return self.board.count(2) == 0

    def create_simulation_copy(self):
        return Ledge(deepcopy(self.board), self.current_player)

    def get_state(self):
        return (tuple(self.board), self.current_player)
        
    