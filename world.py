from pybrain.rl.environments.environment import Environment
from dataset import data
import random

""" This class implements the basic environment, which contains the components of the
  environments such as the animats, food and non-food
"""
class World(Environment):

    """   Number of action/motor values the environment accepts:
          1. leg motor
          2. mouth motor
    """
    indim = 2

    """   Number of sensor values the environment produces:
          1. smell of food
          2. smell of non-food
    """
    outdim = 2

    """   Number of actions(state) the animats have:
          1. idle
          2. move and eat
    """
    numActions = 2

    def __init__(self, sub_env):
        self.sub_env = sub_env
        self.stupid_animats = []

    def getSensors(self):
        #random.seed()
        #sensors = data[random.randint(0, 14)][0]
        sensors = (1, 1, 0, 0)
        return sensors

    def performAction(self, action):
        pass

    def reset(self):
        pass

    def add_agent(agent):
        pass



