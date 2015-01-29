from pybrain.rl.agents import LearningAgent
from world import World
import cell
import math
import random

class StupidAnimat(LearningAgent):
    SenseFoodRadius = 10
    MaxEnergy = 1000
    Speeds = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    Size = 10
    MaxAge = 2000

    def __init__(self, x, y, brain, learner, env):
        LearningAgent.__init__(self, brain.net, learner)
        self.cellType = 3
        self.brain = brain
        self.module = brain.net
        self.learner = learner
        self.env = env
        self.color = cell.BLACK
        self.x = x
        self.y = y
        self.num_interactions = 0
        self.age = 0
        self.colddown = 0

        self.speed = self.Speeds[0]
        self.energy = self.MaxEnergy
        self.food_sensor = 0;
        self.hunger_sensor = 0;
        self.target = [-1, -1]

    def moveInDirection(self, direction):
        nextX = self.x + self.Speeds[direction][0]
        nextY = self.y + self.Speeds[direction][1]
        if self.env.grids[nextX][nextY].isWall():
            direction = (direction + 2) % 4

        self.x += self.Speeds[direction][0]
        self.y += self.Speeds[direction][1]
        self.energy -= 1

    def moveTowardsTarget(self, x, y):
        direction = -1
        minDist = self.calDistance(self.x, self.y, x, y)
        for i in range(4):
            nextX = self.x + self.Speeds[i][0]
            nextY = self.y + self.Speeds[i][1]
            if self.calDistance(nextX, nextY, x, y) < minDist:
                direction = i
                minDist = self.calDistance(self.x, self.y, nextX, nextY)
        if direction >= 0:
            self.moveInDirection(direction)

        print direction
        if minDist - 0 < 0.001:
            self.target = [-1, -1]
            return True
        else:
            return False

    def turnBackward(self):
        if self.speed[0] != 0:
            self.speed[0] *= -1
        elif self.speed[1] != 0:
            self.speed[1] *= -1

    def calDistance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


    def get_sensors(self):
        foods = self.env.foods
        non_foods = self.env.nonfoods
        min_dist = 1000.0
        self.food_sensor = 0

        if (self.energy < 0.8 * self.MaxEnergy):
            self.hunger_sensor = 1
        else:
            self.hunger_sensor = 0

        # search for nearest food
        for food in foods:
            curr_dist = self.calDistance(self.x, self.y, food.x, food.y)
            if curr_dist <= self.SenseFoodRadius:
                self.food_sensor = 2
                if curr_dist <= min_dist:
                    self.target[0] = food.x
                    self.target[1] = food.y
                    min_dist = curr_dist

        # didn't sense any food, search for nearest non-food
        min_dist = 1000.0
        if self.food_sensor != 2:
            for non_food in non_foods:
                curr_dist = self.calDistance(self.x, self.y, non_food.x, non_food.y)
                if curr_dist <= self.SenseFoodRadius:
                    self.food_sensor = 1
                    if curr_dist <= min_dist:
                        self.target[0] = non_food.x
                        self.target[1] = non_food.y
                        min_dist = curr_dist

        if self.food_sensor == 0:
            self.target = [-1, -1]
        sensors = (self.hunger_sensor, self.food_sensor)
        print self.target
        print sensors
        # This is needed for the internal library
        self.integrateObservation(sensors)

        # Determine if we need the animat to learn from experience
        if (self.food_sensor == 1 and self.hunger_sensor == 1):
            self.learning = True
        else:
            self.learning = False

        return sensors

    def get_actions(self):
        return self.getAction()

    def perform_action(self, actions):
        mouth = actions[0]
        # Mouth motor activated, move to target and eat
        if mouth >= 0.8 and mouth <= 1.2 and self.target != [-1, -1]:
            print "moving to target"
            if self.moveTowardsTarget(self.target[0], self.target[1]):
                self.eat()
        else:
            print actions
            print self.energy
            print self.age
            self.moveInDirection(random.randint(0, 3))

    def eat(self):
        if self.food_sensor == 2:
            self.energy += self.MaxEnergy * 0.3
            if self.energy > self.MaxEnergy:
                self.energy = self.MaxEnergy

