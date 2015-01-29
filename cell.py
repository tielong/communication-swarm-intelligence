
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class Cell():
	Size = 10
	def __init__(self, cellType, color):
		self.cellType = cellType
		self.color = color


	def isWall(self):
		return self.cellType == -1

	def isFood(self):
		return self.cellType == 1

	def isNonFood(self):
		return self.cellType == 2

	def isAnimat(self):
		return self.cellType == 3


class Wall(Cell):
	def __init__(self):
		self.cellType = -1
		self.color = BLACK

class Road(Cell):
	def __init__(self):
		self.cellType = 0
		self.color = WHITE
