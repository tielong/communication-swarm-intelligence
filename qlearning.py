#!/usr/bin/python

#from numpy import *
import random

class State():
	SenseNothing = 0
	SenseFood = 1
	SenseNonFood = 2
	SenseFoodAndNonFood = 3
	Hungry = True
	NotHungry = False


class Action():
	MoveRandomly = 0
	MoveTowardsFood = 1
	MoveTowardsNonFood = 2

class Actions():
	a = {}
	a[(State.Hungry, State.SenseNothing)] = [Action.MoveRandomly]
	a[(State.NotHungry, State.SenseNothing)] = [Action.MoveRandomly]
	a[(State.Hungry, State.SenseFood)] = [Action.MoveRandomly, Action.MoveTowardsFood]
	a[(State.NotHungry, State.SenseFood)] = [Action.MoveRandomly, Action.MoveTowardsFood]
	a[(State.Hungry, State.SenseNonFood)] = [Action.MoveRandomly, Action.MoveTowardsNonFood]
	a[(State.NotHungry, State.SenseNonFood)] = [Action.MoveRandomly, Action.MoveTowardsNonFood]
	a[(State.Hungry, State.SenseFoodAndNonFood)] = [Action.MoveRandomly, Action.MoveTowardsFood, Action.MoveTowardsNonFood]
	a[(State.NotHungry, State.SenseFoodAndNonFood)] = [Action.MoveRandomly, Action.MoveTowardsFood, Action.MoveTowardsNonFood]



class QLearn():
	
	def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
		self.q = {}
		
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		self.actions = actions
		self.lastAction = None

		#self.q[((1, 1), 1)] = 1

	def setQ(self, state, action, value):
		self.q[(state,action)] = value

	def getQ(self, state, action):
		return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

	def learnQ(self, state, action, reward, value):
		oldv = self.q.get((state, action), None)
		if oldv is None:
			self.q[(state, action)] = reward
		else:
			self.q[(state, action)] = oldv + self.alpha * (value - oldv)

	def chooseAction(self, state, return_q=False):
		#q = [self.getQ(state, a) for a in self.actions]
		q = [self.getQ(state, a) for a in Actions.a[state]]
		maxQ = max(q)

		if random.random() < self.epsilon:
			minQ = min(q); mag = max(abs(minQ), abs(maxQ))
			#q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] # add random values to all the actions, recalculate maxQ
			q = [q[i] + random.random() * mag - .5 * mag for i in range(len(Actions.a[state]))]
			maxQ = max(q)

		count = q.count(maxQ)

		if count > 1:
			#best = [i for i in range(len(self.actions)) if q[i] == maxQ]
			best = [i for i in range(len(Actions.a[state])) if q[i] == maxQ]
			i = random.choice(best)
		else:
			i = q.index(maxQ)

		#action = self.actions[i]
		action = Actions.a[state][i]

		if return_q: # if they want it, give it!
			return action, q

		return action

	def learn(self, state1, action1, reward, state2):
		#maxqnew = max([self.getQ(state2, a) for a in self.actions])
		maxqnew = max([self.getQ(state2, a) for a in Actions.a[state2]])
		self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)

	def printQ(self):
		
		keys = self.q.keys()
		states = list(set([a for a,b in keys]))
		actions = list(set([b for a,b in keys]))

		dstates = ["".join([str(int(t))+" " for t in list(tup)]) for tup in states]
		print (" "*4) + " ".join(["%8s" % ("("+s+")") for s in dstates])
		for a in actions:
			print ("%3d " % (a)) + \
			" ".join(["%8.2f" % (self.getQ(s,a)) for s in states])
		

