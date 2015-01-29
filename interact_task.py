from pybrain.rl.environments import EpisodicTask
from world import World

actions = [
        (0, 0, 0),  # IDLE
        (0, 1, 1),  # MATE
        (1, 0, 1),  # EAT
]


class InteractTask(EpisodicTask):
    def __init__(self, env, animat):
        EpisodicTask.__init__(self, env)
        self.animat = animat

    def reset(self):
        EpisodicTask.reset(self)
        self.total_reward = 0.0

    def performAction(self, action):
        EpisodicTask.performAction(self, action)

    def getReward(self):
        sensors = self.animat.lastobs
        action = self.animat.lastaction
        # we are only interested in differentiating food and non-food
        is_hungry = sensors[0]
        smell = sensors[1]
        reward = 0
        if is_hungry == 1 and smell == 2:
            # reward agent if sensing food and move towards it
            mouth = action[0]
            if mouth >= 0.95 and mouth <= 1.05:
                reward = 1000
        if is_hungry == 1 and smell == 1:
            # punish the agent if sensing non-food and move towards it
            mouth = action[0]
            if mouth > 0.5:
                reward = -1000
            elif mouth > 0.2 and mouth <= 0.5:
                reward = 10
            elif mouth >= 0.0 and mouth <= 0.2:
                reward = 10000

        #print reward
        return reward

