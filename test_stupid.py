from interact_task import InteractTask
from brain_controller import BrainController
from world import World
from stupid_animat import StupidAnimat
from environment import Environment
from pybrain.rl.learners import Q, ENAC, Reinforce
from pybrain.rl.experiments import Experiment
from pybrain.rl.agents import LearningAgent
import pickle
import time

# Create environment
sub_env = Environment(20, 20)
world = World(sub_env)

# Brain for the animat, we have already trained the data
f = open('neuro.net', 'r')
trained_net = pickle.load(f)
brain = BrainController(trained_net)

# Learning method we use
#learner = PolicyGradientLearner()
learner = ENAC()
learner._setLearningRate(0.2)
# Create an animat
animat = StupidAnimat(trained_net, learner, sub_env)

# Establish a task
task = InteractTask(world, animat)

brain.validate_net()
experiment = Experiment(task, animat)
while True:
    experiment.doInteractions(10000)
    animat.learn()
    animat.reset()
    brain.validate_net()
    time.sleep(3)
