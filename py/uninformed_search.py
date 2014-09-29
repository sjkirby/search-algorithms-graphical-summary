from collections import deque
from random import shuffle

#returns the integer representation from a state matrix
def state_value(state):
	sum = 0
	for x in range(3):
		for y in range(3):
			sum = sum*10 + state[x][y]
	return sum

#returns the state matrix from an integer representation
def value_state(num):
	state = [[0 for x in range(3)] for x in range(3)]
	for i in range(9):
		state[(8-i)/3][(8-i)%3] = num % 10
		num = num / 10
	return state

#checks if node or its rotations occur in state set
def is_new(node,states):
	if node.value in states:
		return False
	for r in range(3):
		if state_value(rotate_state(node.state)) in states:
			return False
	return True

#rotates a state
def rotate_state(state):
	return zip(*state[::-1])

#checks if node matches goal state
def is_complete(node,goal):
	return node.value == goal.value

#adds state to explored states
def add_state(node,states):
	states.add(state_value(node.state))

#class to abstract node data
class Node:
	def __init__(this,state, parent, depth, pathcost):
		this.state = state
		this.parent = parent
		this.depth = depth
		this.pathcost = pathcost
		this.value = state_value(state)
		
#create a node (generally should use makeState)
def makeNode(state, parent, depth, pathcost):
    return Node(state,parent,depth,pathcost)

#returns a move state from xy origin and xy target, the result of moving from origin to target
def move(state,tx,ty,fx,fy):
	new_state = [row[:] for row in state]
	new_state[tx][ty] = new_state[fx][fy]
	new_state[fx][fy] = 0
	return new_state
	
#returns a list of all moves from a node, sorted by a heuristic
def moves(node,goal,heuristicsort):
	state = node.state
	for x in range(3):
		for y in range(3):
			if(state[x][y]==0):
				tpos = x*3+y
				out = []
				if x!=0:
					out.append(move(state,x,y,x-1,y))
				if x!=2:
					out.append(move(state,x,y,x+1,y))
				if y!=0:
					out.append(move(state,x,y,x,y-1))
				if y!=2:
					out.append(move(state,x,y,x,y+1))
				
				return heuristicsort(map(lambda x: makeNode(x,node,node.depth+1,node.pathcost+1), out),goal)

#unused generic search function				
def generalSearch(queue, limit, numRuns):
	if queue == []:
		return False
	elif testProcedure(queue[0]):
		outputProcedure(numRuns, queue[0])
	elif limit == 0:
		print "Limit reached"
	else:
		limit -= 1
		numRuns += 1
		generalSearch(expandProcedure(queue[0], queue[1:len(queue)]), limit, numRuns)

#prints the move history
def printmoves(node):
	hist = deque()
	while node.parent:
		hist.appendleft(node)
		node = node.parent
	hist.appendleft(node)
	move = 1
	print len(hist),'moves total'
	for n in hist:
		print "Move",move
		move+=1
		for y in n.state:
			print ''.join(map(str,y))
		print
	
		
numMoves = 0
		
#correct search function, with abstraction of append, pop, and next move heuristic sorting
def gen_search(state,goal,limit,numRuns,appendf,popf,heuristicsort,output=True):
	global numMoves
	states = set()
	ops = deque()
	
	appendf(ops,state)
	depth = 0
	
	while len(ops) != 0:
		node = popf(ops)
		if numRuns == limit:
			print "Limit reached"
			return (False,states)
		if is_complete(node,goal):
			if output:
				printmoves(node)
			return (node.depth,len(states),numRuns)
		if is_new(node,states):
			numRuns +=1
			numMoves +=1
			if numRuns % 1000 == 0:
				if output:
					print numRuns,'nodes attempted'#,',len(states),'unique'
				if len(states) > 110000:
					if output:
						print('Search may fail due to Python memory limits')
			
			add_state(node,states)
			for new_node in moves(node,goal,heuristicsort):
				appendf(ops,new_node)
	print "Memory limit error"
	return (False)
	
		
#a heuristic for a random ordering of next moves
def randomorder(node,goal):
	shuffle(node)
	return node

#create an state (returns a Node with no parent)
def makeState(*args):
	sum = 0
	for x in args:
		if x == "blank":
			x = 0
		sum = sum * 10 + x
	return Node(value_state(sum),None,0,0)
	

#test DFS per specification, calls gen_search
def testDFS(init,goal,limit,output=True):
	if output:
		print("DFS")
	return gen_search(init,goal,limit,0,deque.append,deque.pop,randomorder,output)

#test BFS per specification, calls gen_search	
def testBFS(init,goal,limit,output=True):	
	if output:
		print("BFS")
	return gen_search(init,goal,limit,0,deque.appendleft,deque.pop,randomorder,output)
