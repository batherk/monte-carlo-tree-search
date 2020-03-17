import numpy as np
import random
   
class UCTTree:
    """ Chooses a random action every time, does not learn"""

    def __init__(self, exploration=0):
        self.exploration = exploration
        self.states = {}
        self.state_action_pair = {}
        
    def __contains__(self, state):
        return state in self.states

    def default_action(self, game):
        """
        This method takes the argument game and returns an action in its given state. 
        """
        actions = game.get_possible_actions()
        return random.choice(actions)

    def get_max_action_value(self, state, action):
        return self.state_action_pair[(state,action)]["Q"] + self.get_exploration_bonus(state, action)

    def get_min_action_value(self, state, action):
        return self.state_action_pair[(state,action)]["Q"] - self.get_exploration_bonus(state, action)

    def get_exploration_bonus(self, state, action):
        if not self.state_action_pair[(state,action)]["N"]:
            return 0
        temp = np.log(self.states[state]["N"])/self.state_action_pair[(state,action)]["N"]
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
        self.state_action_pair[(state,action)]["N"] += 1
        self.state_action_pair[(state,action)]["Q"] = (result-self.state_action_pair[(state,action)]["Q"])/self.state_action_pair[(state,action)]["N"]



        
    
    def add_state(self, game, state):
        actions = game.get_possible_actions()
        self.states[state] = {"N":0,"A":actions}
        for action in actions:
            self.state_action_pair[(state,action)] = {"N":0,"Q":0}

    def clean():
        self.states = {}


  
        
            