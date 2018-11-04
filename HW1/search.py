# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from game import Directions

    fringe = util.Stack()
    visitedList = []

    #push to stack
    fringe.push((problem.getStartState(),[],0))
    #pop
    (state,toDirection,toCost) = fringe.pop()
    #add to checked list
    visitedList.append(state)

    #while the G is not found get the node's children
    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state) 
        for son in successors:
            #if the child's not been checked push it to stack and then add the node to the checked list
            if (not son[0] in visitedList) or (problem.isGoalState(son[0])):
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                visitedList.append(son[0])
        (state,toDirection,toCost) = fringe.pop()

    return toDirection

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
     from game import Directions
        
    fringe = util.Queue()
    visitedList = []

    #push
    fringe.push((problem.getStartState(),[],0))
    #pop
    (state,toDirection,toCost) = fringe.pop()
    #add the node to visitedList
    visitedList.append(state)
   
    # whiile the goal isn't found its chidren get expanded
    while not problem.isGoalState(state): 
        successors = problem.getSuccessors(state) 
        for son in successors:
            #if the child isn't checked push
            if not son[0] in visitedList: 
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2])) 
                # add
                visitedList.append(son[0]) 
        (state,toDirection,toCost) = fringe.pop()

    return toDirection
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
        from game import Directions

    fringe = util.PriorityQueue() 
    visitedList = []

    #push to queue
    fringe.push((problem.getStartState(),[],0),0) # push starting point with priority num of 0
    #pop 
    (state,toDirection,toCost) = fringe.pop()
    #add to list
    visitedList.append((state,toCost))

    while not problem.isGoalState(state):
        successors = problem.getSuccessors(state)
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                # the point gets added if either the child's not checked or has been checked with a higher price
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True # the node we wanted is checked
                    break

            if not visitedExist:        
                # push based on its total cost and then add to list
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2]) 
                visitedList.append((son[0],toCost + son[2]))

        (state,toDirection,toCost) = fringe.pop()

    return toDirection
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
       from game import Directions

    fringe = util.PriorityQueue() 
    visitedList = []

    fringe.push((problem.getStartState(),[],0),0 + heuristic(problem.getStartState(),problem)) # push starting point with priority num of 0
    (state,toDirection,toCost) = fringe.pop()
    visitedList.append((state,toCost + heuristic(problem.getStartState(),problem)))

    while not problem.isGoalState(state): 
        successors = problem.getSuccessors(state)
        for son in successors:
            visitedExist = False
            total_cost = toCost + son[2]
            for (visitedState,visitedToCost) in visitedList:
                #If the child's not been checked or if it's been checked with a higher cost
                if (son[0] == visitedState) and (total_cost >= visitedToCost): 
                    visitedExist = True
                    break

            if not visitedExist:        
                # push based on the totsl cost and add to the checked list
                fringe.push((son[0],toDirection + [son[1]],toCost + son[2]),toCost + son[2] + heuristic(son[0],problem)) 
                visitedList.append((son[0],toCost + son[2])) 

        (state,toDirection,toCost) = fringe.pop()

    return toDirection
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
