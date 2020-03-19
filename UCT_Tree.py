import numpy as np
import random
   
class UCTTree:
    """ Chooses a random action every time, does not learn"""

    def __init__(self, exploration=0):
        self.exploration = exploration
        self.states = {}
        self.state_action_pairs = {}
        
    def __contains__(self, state):
        return state in self.states

    def Q(self,state,action):
        """ Q value of a state-action pair """
        return self.state_action_pairs[(state,action)]["Q"]
    
    def N(self, state, action=None):
        """ Number of times visited for a state or a state-action pair"""
        if not action:
            return self.states[state]["N"]
        else:
            return self.state_action_pairs[(state,action)]["N"]

    def default_action(self, game):
        """
        This method takes the argument game and returns an action in its given state. 
        """
        actions = game.get_possible_actions()
        return random.choice(actions)

    def get_max_action_value(self, state, action):
        return self.Q(state,action) + self.get_exploration_bonus(state, action)

    def get_min_action_value(self, state, action):
        return self.Q(state,action) - self.get_exploration_bonus(state, action)

    def get_exploration_bonus(self, state, action):
        if not self.N(state,action):
            return 0
        temp = np.log(self.N(state))/self.N(state,action)
        return self.exploration * np.sqrt(temp)

    def select_action(self, game):
        state = game.get_state()
        actions = game.get_possible_actions()

        if game.current_player ==1:
            values = [self.get_max_action_value(state,action) for action in actions]
            index = values.index(max(values))
        else:
            values = [self.get_min_action_value(state,action) for action in actions]
            index = values.index(min(values))

        return actions[index]

    def update(self, state, action, result):
        self.states[state]["N"] += 1
        self.state_action_pairs[(state,action)]["N"] += 1
        self.state_action_pairs[(state,action)]["Q"] += (result-self.Q(state,action))/self.N(state,action)

    def add_state(self, game, state):
        actions = game.get_possible_actions()
        self.states[state] = {"N":0,"A":actions}
        for action in actions:
            game_copy = game.create_simulation_copy()
            game_copy.perform_action(action)
            self.state_action_pairs[(state,action)] = {"N":0,"Q":0,"State":game_copy.get_state()}

    def traverse(self, game):
        game_copy = game.create_simulation_copy()
        sequence = []
        while not game_copy.is_done() or game_copy.get_state() in self:
            sequence.append(game_copy.get_state())
            action = self.select_action(game_copy)
            game_copy.perform_action(action)
        sequence.append(game_copy.get_state())
        return sequence

    def print_qs(self):
        for state in self.states:
                print(state)
                for action in self.states[state]["A"]:
                    print(action, self.state_action_pairs[(state,action)])
                print()
    
    def clean(self):
        self.states = {}


  
        
            