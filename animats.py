import cell
import qlearning
import math
import random

actionNum = 3

class Animat(cell.Cell):
	SenseFoodRadius = 10
	MaxEnergy = 1000
	Speeds = [[0, 1], [1, 0], [0, -1], [-1, 0]]

	def __init__(self, x, y, env):
		self.cellType = 3
		self.color = cell.BLUE
		self.env = env

		self.x = x
		self.y = y
		self.speed = self.Speeds[0]

		self.energy = self.MaxEnergy

		self.ai = qlearning.QLearn(actions = range(actionNum))
		self.lastState = None
		self.lastAction = None
		self.executingAction = False

	def move(self):
		nextX = self.x + self.speed[0]
		nextY = self.y + self.speed[1]
		if self.env.grids[nextX][nextY].isWall():
			self.turnBackward()
		self.x = self.x + self.speed[0]
		self.y = self.y + self.speed[1]

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

		#return True is next position is the target
		if minDist - 0 < 0.001:
			return True
		else:
			return False

	def turnBackward(self):
		if self.speed[0] != 0:
			self.speed[0] *= -1
		elif self.speed[1] != 0:
			self.speed[1] *= -1

	def senseFood(self, foods):
		foodToPick = None
		minDist = self.SenseFoodRadius + 1
		for food in foods:
			dist = self.calDistance(self.x, self.y, food.x, food.y)
			if  dist < minDist and dist < self.SenseFoodRadius:
				minDist = dist
				foodToPick = food
		return foodToPick


	def senseSignal(self, signals):
		return False

	def isHungry(self):
		if self.energy * 1.0 / self.MaxEnergy < 0.8:
			return True
		else:
			return False

	def eat(self):
		self.energy += self.MaxEnergy * 0.3
		if self.energy > self.MaxEnergy:
			self.energy = self.MaxEnergy

	def update(self, foods, nonfoods):
		if self.executingAction == True:
			"""print "executingAction" + str(self.lastAction)"""
			self.decodeAndExecuteAction(self.lastAction, foods, nonfoods)
		else:
			"""print "not executingAction"""
			state = self.calState(foods, nonfoods)
			"""print "energy = " + str(self.energy) + " state = " + str(state)"""
			food = self.senseFood(foods)
			nonfood = self.senseFood(nonfoods)
			reward = 0
			if food is not None and self.x == food.x and self.y == food.y and self.lastAction != 0:
				if self.isHungry():
					reward = 100
				else:
					reward = -50
				self.eat()

			if nonfood is not None and self.x == nonfood.x and self.y == nonfood.y and self.lastAction != 0:
				reward = -100

			if self.lastState is not None:
				self.ai.learn(self.lastState, self.lastAction, reward, state)				
			
			self.lastState = self.calState(foods, nonfoods)
			self.lastAction = self.ai.chooseAction(state)

			#self.moveInDirection(self.lastAction)
			self.decodeAndExecuteAction(self.lastAction, foods, nonfoods)

	def calDistance(self, x1, y1, x2, y2):
		return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

	def calState(self, foods, nonfoods):
		food = self.senseFood(foods)
		nonfood = self.senseFood(nonfoods)
		if food is None and nonfood is None:
			return self.isHungry(), 0
		elif food is not None and nonfood is None:
			return self.isHungry(), 1
		elif food is None and nonfood is not None:
			return self.isHungry(), 2
		else:
			return self.isHungry(), 3

	def decodeAndExecuteAction(self, action, foods, nonfoods):
		if action == 0: #move randomly
			self.moveInDirection(random.randrange(0, 4))
		elif action == 1:  #move towards food
			food = self.senseFood(foods)
			if food != None:
				if self.executingAction is False:
					self.executingAction = True
				if self.moveTowardsTarget(food.x, food.y):
					self.executingAction = False
			else:
				self.moveInDirection(random.randrange(0, 4))
		elif action == 2: #move towards nonfood
			nonfood = self.senseFood(nonfoods)
			if nonfood != None:
				if self.executingAction is False:
					self.executingAction = True
				if self.moveTowardsTarget(nonfood.x, nonfood.y):
					self.executingAction = False
			else:
				self.moveInDirection(random.randrange(0, 4))
