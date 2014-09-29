from Queue import PriorityQueue
from collections import deque
from random import shuffle
import time

uninformed = __import__('sjkirbyhw2-uninformed')

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
def moves(node,goal,pathcost):
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
				
				return map(lambda x: makeNode(x,node,node.depth+1,pathcost(node,goal)), out)

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

numMoves = 0
		
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
	
		
#correct search function, with abstraction of path cost heuristic (is only cumulative for A*)
def gen_search(state,goal,limit,numRuns,pathcost,output=True):
	global numMoves
	states = set()
	ops = PriorityQueue()
	
	ops.put((state.pathcost,state))
	
	while not ops.empty():
		node = ops.get()[1]
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
			for new_node in moves(node,goal,pathcost):
				ops.put((new_node.pathcost,new_node))
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

#hammingDistance formula to compare number values
def hammingDistance(node,goal):
	score = 0
	val1 = node.value
	val2 = goal.value
	for i in range(9):
		if val1 %10 != val2 %10:
			score +=1
		val1 = val1 / 10
		val2 = val2 / 10
	return score

#hammingDistance formula that sums with previous pathcost
def hammingCumulative(node,goal):
	score = node.pathcost
	val1 = node.value
	val2 = goal.value
	for i in range(9):
		if val1 %10 != val2 %10:
			score +=1
		val1 = val1 / 10
		val2 = val2 / 10
	return score

#distance between each number position across numerical representation
def generalDistance(node,goal):
	score = 0
	val1 = node.value
	val2 = goal.value
	for i in range(9):
		score += abs((val1%10) - (val2%10))
		val1 = val1 / 10
		val2 = val2 / 10
	return score

#distance between total numerical representations
def totalDistance(node,goal):
	score = 0
	val1 = node.value
	val2 = goal.value
	return abs(val1 - val2)
	
	
#test InformedSearch1 per specification, using hammingDistance
def testInformedSearch1(init,goal,limit,output=True):
	if output:
		print("Informed Search 1")
	return gen_search(init,goal,limit,0,hammingDistance,output)

#test InformedSearch2 per specification, using overall node value
def testInformedSearch2(init,goal,limit,output=True):	
	if output:
		print("Informed Search 2")
	return gen_search(init,goal,limit,0,totalDistance,output)

#test A* per specification, using a cumulative hammingDistance
def testAStar(init,goal,limit,output=True):	
	if output:
		print("A*")
	return gen_search(init,goal,limit,0,hammingCumulative,output)




#random trials for question 2 and 3, gathers data on cases where all trials succeed.
def semi_random_trials(num_trials):
	stats = []
	initialState = makeState(375186402)
	goalState = makeState(123456789)
	semiRandomStates = uninformed.testDFS(initialState, goalState, 100000)
	semiRandomStates = list(semiRandomStates[-1])
	shuffle(semiRandomStates)
	testStates = semiRandomStates[:num_trials]

	searchTests = [uninformed.testBFS,
					 uninformed.testDFS,
					 testInformedSearch1,
					 testInformedSearch2,
					 testAStar]
					 

	goalState = makeState(123456780)
	for searchTest in searchTests:
		stats.append([])
		for i in range(num_trials):
			testVal = testStates[i]
			testNode = makeState(testVal)
			stats[-1].append(searchTest(testNode,goalState,10000000,False))
			print len(stats),len(stats[-1])
			
	names = 'abcde'



	def isvalid(stats, i):
		valid = True
		for x in range(5):
			valid = valid and stats[x][i] and stats[x][i][0]
		return valid
			

	valid = []
	for i in range(num_trials):
		if isvalid(stats,i):
			valid.append(i)
			
	for i in range(5):
		name = names[i]
		print name,'= ['
		for x in valid:
			x = stats[i][x]
			print x[0],',',x[1],',',pow(x[1],(1.0 / (x[0] * 1.0))),';'
		print ']'
	return valid
		
#test_stats = semi_random_trials(250)

#timing tests for question 4
def run_tests():
	goalState = makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank")

	tests = []
	# First group of test cases - should have solutions with depth <= 5
	initialState = makeState(375186402)

	tests.append(makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8))
	tests.append(makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8))
	tests.append(makeState(1, 2, 3, 4, 5, 6, 7, "blank", 8))
	tests.append(makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8))
	tests.append(makeState(1, 2, 3, 4, 8, 5, 7, "blank", 6))


	# Second group of test cases - should have solutions with depth <= 10
	tests.append(makeState(2, 8, 3, 1, "blank", 5, 4, 7, 6))
	tests.append(makeState(1, 2, 3, 4, 5, 6, "blank", 7, 8))
	tests.append(makeState("blank", 2, 3, 1, 5, 6, 4, 7, 8))
	tests.append(makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8))
	tests.append(makeState(1, 3, "blank", 4, 2, 5, 7, 8, 6))


	# Third group of test cases - should have solutions with depth <= 20
	tests.append(makeState("blank", 5, 3, 2, 1, 6, 4, 7, 8))
	tests.append(makeState(5, 1, 3, 2, "blank", 6, 4, 7, 8))
	tests.append(makeState(2, 3, 8, 1, 6, 5, 4, 7, "blank"))
	tests.append(makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8))
	tests.append(makeState("blank", 3, 6, 2, 1, 5, 4, 7, 8))


	# Fourth group of test cases - should have solutions with depth <= 50
	tests.append(makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8))
	tests.append(makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4))
	tests.append(makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7))
	tests.append(makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7))
	tests.append(makeState(3, 8, 5, 1, 6, 7, 4, 2, "blank"))

	searchTests = [uninformed.testBFS,
					 uninformed.testDFS,
					 testInformedSearch1,
					 testInformedSearch2,
					 testAStar]
	
	for search in searchTests:
		start = time.time()
		ops = 0;
		for test in tests:
			result = search(test,goalState,100000,False)
			if result and result[0]:
				ops += result[1]
			else:
				ops += 100000
		end = time.time()
		print ops,end-start,ops / ((end-start) / (5.0 * 60))

#produces sample output for required documents		
def sample_output():
	searchTests = [uninformed.testBFS,
					 uninformed.testDFS,
					 testInformedSearch1,
					 testInformedSearch2,
					 testAStar]
	for search in searchTests:
		search(makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8),makeState(1, 2, 3, 4, 5, 6, 7, 8, "blank"),100000)
		
