#Last Edit 2019-02-19
#This program will solve the 8 puzzle "game" by using A* search.
#Made by Kristoffer Grahn


import math
import random
import copy



class Board():
	def __init__(self,start_state, gCost, cameFrom = None):
		self.state = start_state
		self.goal_state = [[0,1,2],[3,4,5],[6,7,8]]

		if cameFrom is None:
			self.parent = None
		else:
			self.parent = cameFrom

		self.gCost = gCost
		self.hCost = self.calculateScore()
		
	def isGoal(self):
		return stateCompare(self.state,self.goal_state)
		
	
	def solve(self):
		self.a_star()

	def moveLeft(self,x,y,):
		
		new_state = copy.deepcopy(self.state)

		new_state[x][y] = new_state[x][y - 1]
		new_state[x][y - 1] = 0

		return new_state

	def moveRight(self,x,y):
		new_state = copy.deepcopy(self.state)

		new_state[x][y] = new_state[x][y + 1]
		new_state[x][y + 1] = 0

		return new_state

	def moveUp(self,x,y):
		new_state = copy.deepcopy(self.state)

		new_state[x][y] = new_state[x - 1][y]
		new_state[x - 1][y] = 0

		return new_state

	def moveDown(self,x,y):
		new_state = copy.deepcopy(self.state)

		new_state[x][y] = new_state[x + 1][y]
		new_state[x + 1][y] = 0

		return new_state

	def createSuccessor(self):
		successorList = []

		
		x,y = findIndex(self.state,0)

		if x < 2:
			successorList.append(Board(self.moveDown(x,y),self.gCost + 1,self))
		if x > 0:
			successorList.append(Board(self.moveUp(x,y),self.gCost + 1 ,self))
		if y > 0:
			successorList.append(Board(self.moveLeft(x,y),self.gCost + 1 ,self))
		if y < 2:
			successorList.append(Board(self.moveRight(x,y),self.gCost + 1,self))

		if self.parent is None:
			return successorList
		else:
			
			for obj in successorList:
				if stateCompare(obj.parent.parent.state,obj.state):
				
					successorList.pop(findObjectInList(obj,successorList))
			return successorList

	def reconstructPath(self):

		pathList = [self.state]
		pointer = self

		while (pointer.parent != None):
			pointer = pointer.parent
			pathList.insert(0,pointer.state)
		

		return pathList


	def a_star(self):
		frontier = []
		explored = []
		

		cameFrom = self
		gCost = self.gCost
		hCost = self.hCost
		goal_state = self.goal_state
		count = 0
		
		frontier.append(self)

		while(frontier) :
			
			
			currentBoard = pickBestFrontier(frontier)

			frontier.pop(findObjectInList(currentBoard,frontier))
			explored.append(currentBoard)

			#print("Current board: ",currentBoard.state, " gCost:" , currentBoard.gCost, " hCost", currentBoard.hCost)

			if (currentBoard.isGoal()):

				
				print("Goal Found, explored nodes: ",len(explored))
				print(currentBoard.reconstructPath())
				return


	
			successors = currentBoard.createSuccessor()

			for obj in successors:
				

				if obj in explored:

					for ex in explored:
						if obj == ex:
							if obj.gCost + obj.hCost < ex.hCost + ex.gCost:
								ex.gCost = obj.gCost
								ex.hCost = obj.hCost
								ex.parent = obj.parent
								frontier.insert(0,ex)

								
								explored.pop(findObjectInList(ex,explored))
								

					return
					

				elif obj in frontier:
					
					for front in frontier:
						if obj == front:
							if obj.gCost + obj.hCost < front.hCost + front.gCost:
								front.gCost = obj.gCost
								front.hCost = obj.hCost
								front.parent = obj.parent
								


				else:
					frontier.append(obj)




	def calculateScore(self):
		hCost = 0

		for x in range(len(self.state)):
				for y in range(len(self.state[0])):
					
					if self.state[x][y] != self.goal_state[x][y]:
						if self.state[x][y] != 0:
							x_goal, y_goal = findIndex(self.goal_state,self.state[x][y])
							hCost += abs(x_goal - x) + abs(y_goal - y)
		return hCost


def findIndex(state,index):
	for x in range(len(state)):
			if index in state[x]:
				for y in range(len(state[x])):
					if index == state[x][y]:
						return (x,y) #return the coordinates for the index.
	return -1,-1 #If no index is found, return -1 and -1



def pickBestFrontier(frontier):

	if len(frontier) == 1:
		return frontier[0]

	board = frontier[0]

	for i in range(len(frontier)):
		if board.hCost + board.gCost >= frontier[i].hCost + frontier[i].gCost:
			board  = frontier[i]

	return board

def stateCompare(state,goal_state):
	for x in range(len(state)):
		for y in range(len(state)):
			if state[x][y] != goal_state[x][y]:
				return False
	return True

def findObjectInList(object,List):
	if len(List) == 1:
		return 0

	for x in range(len(List)):
		if object == List[x]:
			return x


def main():
	
	start_state = [[7,2,4],[5,0,6],[8,3,1]]
	state2 = [[4,8,5],[3,7,2],[1,6,0]]
	goal_state = [[0,1,2],[3,4,5],[6,7,8]]

	board = Board(start_state,0)
	board.solve()
	
	


main()
