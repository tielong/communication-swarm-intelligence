from cell import *
from animats import *
from food import *

from interact_task import InteractTask
from brain_controller import BrainController
from world import World
from stupid_animat import StupidAnimat
from pybrain.rl.learners import Q, ENAC, Reinforce
from pybrain.rl.experiments import Experiment
from pybrain.rl.agents import LearningAgent
import pickle
import time

class Environment():
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.grids =  [[None for col in range(w)] for row in range(h)]
        self.initGrids(w, h)
        self.animats = []

        self.stupid_animats = []
        self.tasks = []
        self.foods = []
        self.nonfoods = []

    def initGrids(self, w, h):
        for i in range(w):
            for j in range(h):
                if i == 0 or j ==0 or i == w-1 or j == h-1:
                    self.grids[i][j] = Wall()
                else:
                    self.grids[i][j] = Road()

    def createAnimats(self):
        a = Animat(9,9, self)
        self.animats.append(a)
        #a = Animat(21,21, self)
        #self.animats.append(a)


    def createStupidAnimat(self, x, y):
        f = open('neuro.net', 'r')
        trained_net = pickle.load(f)
        learner = ENAC()
        learner._setLearningRate(0.03)
        brain = BrainController(trained_net)
        new_x = x + random.randint(-3, 3)
        if new_x > 79:
            new_x = 79
        elif new_x < 0:
            new_x = 0
        new_y = y + random.randint(-3, 3)
        if new_y > 79:
            new_y = 79
        elif new_y < 0:
            new_y = 0
        sa = StupidAnimat(new_x, new_y, brain, learner, self)
        sa.brain.validate_net()
        world = World(self)
        task = InteractTask(world, sa)
        self.stupid_animats.append(sa)
        self.tasks.append(task)

    def createFoods(self, num):
        for i in range(1):
            self.foods.append(Food(40, 40))

    def createNonFoods(self, num):
        for i in range(num):
            self.nonfoods.append(NonFood(i*5, self.height - i*5))

    def update(self):
        for i in range(len(self.animats)):
            self.animats[i].update(self.foods, self.nonfoods)

        for i in range(len(self.stupid_animats)):
            curr_animat = self.stupid_animats[i]
            sensors = curr_animat.get_sensors()
            curr_animat.perform_action(curr_animat.get_actions())
            reward = self.tasks[i].getReward()
            curr_animat.giveReward(reward)
            curr_animat.num_interactions += 1
            curr_animat.age += 1
            if curr_animat.colddown < 100:
                curr_animat.colddown += 1
            if curr_animat.age >= 0.4 * curr_animat.MaxAge and curr_animat.age <= 0.5 * curr_animat.MaxAge:
                if curr_animat.energy >= 0.6 * curr_animat.MaxEnergy:
                   if curr_animat.colddown == 100:
                       self.createStupidAnimat(curr_animat.x, curr_animat.y)
                       curr_animat.energy = curr_animat.energy - 0.5 * curr_animat.energy
                       curr_animat.colddown = 0
            if curr_animat.num_interactions == 120:
                curr_animat.learn()
                curr_animat.num_interactions = 0

        for i in range(len(self.animats)):
            if i >= len(self.animats):
                break
            if self.animats[i].energy <= 0:
                self.animats[i].ai.printQ()
                self.animats.pop(i)

        for i in range(len(self.stupid_animats)):
            if i >= len(self.stupid_animats):
                break
            curr_animat = self.stupid_animats[i]
            if curr_animat.energy <= 0 or curr_animat.age == curr_animat.MaxAge:
                curr_animat.brain.validate_net()
                self.stupid_animats.pop(i)
                self.tasks.pop(i)


