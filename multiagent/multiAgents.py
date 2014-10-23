# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        capsuleList = successorGameState.getCapsules()
        foodList = newFood.asList()
                
        
        minD = 1000
        mind = 1000
        for n in foodList:    
            if util.manhattanDistance(newPos, n) < minD:
                minD = util.manhattanDistance(newPos, n)
        if len(capsuleList) == 0:
            mind = 1000
        for n in capsuleList:
            if util.manhattanDistance(newPos, n) < mind:
                mind = util.manhattanDistance(newPos, n)
        if len(newGhostStates) == 1:
            safety = util.manhattanDistance(newPos,newGhostStates[0].getPosition())
        count = len(foodList)
        count1 = len(capsuleList)+1
        if newScaredTimes[0] > 1:
            return  10/(count+1)+10/(minD+1)+150/(safety+1) + successorGameState.getScore()+10000/count1
        if newScaredTimes[0] == 0:
            if safety <= 1:
                return 10/(count+1)+10/(minD+1)-1000+ successorGameState.getScore()+400/mind+10000/count1


            if safety <= 2:
                return 10/(count+1)+10/(minD+1)-500 + successorGameState.getScore()+400/mind+10000/count1


            else:
                return 10/(count+1)+10/(minD+1)+ successorGameState.getScore()+400/mind+10000/count1





        

    
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState,0,1,True)    
    def minimax(self, gameState, agentNum, depth, isMaximizer):
        if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
        if isMaximizer:
            bestValue = -10000
            bestAction = "Shoot up heroin"
            for action in gameState.getLegalActions(0):
                nextState = gameState.generateSuccessor(0, action)
                val = self.minimax(nextState,1,depth,False)
                if val > bestValue:
                    bestValue = val
                    bestAction = action
            if depth > 1: return bestValue
            if depth == 1: return bestAction
        else:
            bestValue = 10000
            bestAction = "Candy Flippin"
            numAgents = gameState.getNumAgents()
            for action in gameState.getLegalActions(agentNum):
                nextState = gameState.generateSuccessor(agentNum, action)
                if agentNum<(numAgents-1):
                    val = self.minimax(nextState,agentNum+1,depth,False)
                else:
                    if depth < self.depth:
                        val = self.minimax(nextState,0,depth+1,True)
                    else:
                        val = self.evaluationFunction(nextState)
                if val < bestValue:
                    bestValue = val
        return bestValue

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaPrune(gameState,0,1,-10000,10000,True)
    def alphaBetaPrune(self,gameState, agentNum, depth, alpha, beta, isMaximizer):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if isMaximizer:
            bestValue = -10000
            bestAction = "Drop acid"
            for action in gameState.getLegalActions(agentNum):
                nextState = gameState.generateSuccessor(agentNum, action)
                val = self.alphaBetaPrune(nextState,1,depth,alpha,beta,False)
                if val > beta:
                    return val
                if val > bestValue:
                    bestValue = val
                    bestAction = action
                alpha = max(alpha, bestValue)
            if depth > 1: return bestValue
            if depth == 1: return bestAction
        else:
            bestValue = 10000
            bestAction = "pop Molly"
            for action in gameState.getLegalActions(agentNum):
                nextState = gameState.generateSuccessor(agentNum, action)
                if agentNum<(numAgents-1):
                    val = self.alphaBetaPrune(nextState,agentNum+1,depth,alpha, beta,False)
                else:
                    if depth < self.depth:
                        val = self.alphaBetaPrune(nextState,0,depth+1,alpha,beta,True)
                    else:
                        val = self.evaluationFunction(nextState)
                if alpha > val:
                    bestValue = val
                    break
                if val < bestValue:
                    bestValue = val
                beta = min(beta, bestValue)
            return bestValue
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectiMax(gameState,0,1,True)
    def expectiMax(self, gameState, agentNum, depth, isMaximizer):
        if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
        numAgents = gameState.getNumAgents()
        if isMaximizer:  
            bestValue = -10000
            bestAction = "Smoke meth"
            for action in gameState.getLegalActions(0):
                nextState = gameState.generateSuccessor(0, action)
                val = self.expectiMax(nextState,1,depth,False)
                if val > bestValue:
                    bestValue = val
                    bestAction = action
            if depth > 1: return bestValue
            if depth == 1: return bestAction
        else:
            bestValue = 0
            bestAction = "Snort Adderall"
            for action in gameState.getLegalActions(agentNum):
                nextState = gameState.generateSuccessor(agentNum, action)
                p = 1.0/len(gameState.getLegalActions(agentNum))
                if agentNum<(numAgents-1):
                    val = self.expectiMax(nextState,agentNum+1,depth,False)
                else:
                    if depth < self.depth:
                        val = self.expectiMax(nextState,0,depth+1,True)
                    else:
                        val = self.evaluationFunction(nextState)
                
                bestValue += val
        return bestValue*p



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghosts = currentGameState.getGhostStates()
    numFood = currentGameState.getNumFood()
    score = currentGameState.getScore()
    numAgents = currentGameState.getNumAgents()
    capsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghosts]
    
    minD = 1000
    mind = 1000
    for n in food:    
       if util.manhattanDistance(pos, n) < minD:
            minD = util.manhattanDistance(pos, n)
    if len(capsules) == 0:
        mind = 1000
    for n in capsules:
        if util.manhattanDistance(pos, n) < mind:
            mind = util.manhattanDistance(pos, n)
    if len(ghosts) == 1:
        safety = util.manhattanDistance(pos,ghosts[0].getPosition())
    count = len(food.asList())
    count1 = len(capsules)+1
    if newScaredTimes[0] > 1:
        return  100/(count+1)+7/(minD+1)+150/(safety+1) + currentGameState.getScore()+10000/count1
    if newScaredTimes[0] == 0:
        if safety <= 1:
            return 10/(count+1)+7/(minD+1)-1000+ currentGameState.getScore()+400/mind+10000/count1


        if safety <= 2:
            return 10/(count+1)+7/(minD+1)-500 + currentGameState.getScore()+400/mind+10000/count1


        else:
            return 10/(count+1)+7/(minD+1)+ currentGameState.getScore()+400/mind+10000/count1







# Abbreviation
better = betterEvaluationFunction

