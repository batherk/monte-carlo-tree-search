import numpy as np
import random
   
class UCTTree:
    """ Chooses a random action every time, does not learn"""

    def __init__(self, max=True):
        self.states = {}
        self.state_action_pair = {}
        
    def default_action(self, game):
        """
        This method takes the argument game and returns an action in its given state. 
        """
        actions = game.get_possible_actions()
        return random.choice(actions)

    def select_action(self, state, player):

        for action in self.states[state]["actions"]:
            sum_results = self.states[state]['actions'][action]["sum_results"]
            visited = self.states[state]['actions'][action]["visited"]

            average = sum_results/visited

            if self.max and average > best_value or not self.max and average < best_value:
                best_action = action
                best_value = average
        return best_action

    def update(self, state, action, reward):
        if not state in self.states:
            self.states[state] = {"visited": 0, "actions":{}}
        self.states[state]["visited"] += 1

        if not action in self.states[state]['actions']:
            self.states[state]['actions'][action] = {"visited": 0, "sum_results":0}
        self.states[state]['actions'][action]["visited"] += 1 
        self.states[state]['actions'][action]["sum_results"] += reward
        

    def clean():
        self.states = {}


  
        
            