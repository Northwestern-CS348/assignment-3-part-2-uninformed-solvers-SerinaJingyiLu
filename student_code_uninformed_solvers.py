
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here


        if self.currentState.state == self.victoryCondition or self.currentState not in self.visited:
            self.visited[self.currentState]=True

            return self.currentState.state == self.victoryCondition

        # Expand the new states from the parent state, but do not go through it
        if not self.currentState.children:
            for movable_states in self.gm.getMovables():
                self.gm.makeMove(movable_states)

                NextGameState = GameState(self.gm.getGameState(), self.currentState.depth+1, movable_states)
                if NextGameState not in self.visited:
                    NextGameState.parent = self.currentState
                    self.currentState.children.append(NextGameState)
                self.gm.reverseMove(movable_states)

        if self.currentState.nextChildToVisit<len(self.currentState.children):  #explores as far as possible along each branch before backtracking
            nextState = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(nextState.requiredMovable)
            self.currentState = nextState
            return self.solveOneStep()
        else:    #Backtracking
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStep()












class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            self.visited[self.currentState] = True
            return True

        depth = self.currentState.depth

        while True:
            next = self.solveOneStepOnDepth(depth)
            if next:
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    depth += 1
            else:
                return False

    def solveOneStepOnDepth(self, depth):
        if self.currentState.depth == depth:  # First time to expand a new state
            if self.currentState not in self.visited or depth == 0 and not self.currentState.children:
                for movable_states in self.gm.getMovables():
                    self.gm.makeMove(movable_states)

                    NextGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable_states)
                    if NextGameState not in self.visited:
                        NextGameState.parent = self.currentState
                        self.currentState.children.append(NextGameState)
                    self.gm.reverseMove(movable_states)
            if self.currentState.state == self.victoryCondition or self.currentState not in self.visited:
                self.visited[self.currentState] = True

                return self.currentState.state == self.victoryCondition
            else:
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepOnDepth(depth)

        elif self.currentState.depth < depth:
            if self.currentState.nextChildToVisit > len(self.currentState.children):
                self.currentState.nextChildToVisit = 0
            #self.currentState.nextChildToVisit = 0
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                nextState = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(nextState.requiredMovable)
                self.currentState = nextState

                return self.solveOneStepOnDepth(depth)
            else:
                     # The nextState does not have any children to expand
                self.currentState.nextChildToVisit += 1
                if self.currentState.depth == 0:
                    return True
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent
                return self.solveOneStepOnDepth(depth)



        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.solveOneStepOnDepth(depth)



"""""

        queue = [self.currentState]


        while queue:
            node = queue.pop()

            self.currentState = node
            if self.currentState.requiredMovable:
                self.gm.makeMove(self.currentState.requiredMovable)

            print(self.gm.getGameState())
            self.visited[self.currentState] = True
            if(self.currentState.state==self.victoryCondition):
                return True
            else:
                for movable_states in self.gm.getMovables():
                    self.gm.makeMove(movable_states)

                    NextGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable_states)
                    if(NextGameState in self.visited):
                        continue
                    queue.append(NextGameState)
                    NextGameState.parent = self.currentState
                    self.currentState.children.append(NextGameState)




                    self.gm.reverseMove(movable_states)




"""























