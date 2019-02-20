from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        tuples = ([],[],[])
        listOfBindings = self.kb.kb_ask(parse_input('fact:  (on ?disk ?peg)'))
        for binding in listOfBindings:
            tuples[int(binding['?peg'][3])-1].append(int(binding['?disk'][4]))
        for element in tuples:
             element.sort()
        
        
        return tuple(tuple(e) for e in tuples)
        ### student code goes here


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        retract_facts = []
        assert_facts = []
        
        sl = list(map(lambda x: str(x), movable_statement.terms))
        retract_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[1]+')'))
        assert_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[2]+')'))
        retract_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[1]+')'))
    
        answer = self.kb.kb_ask(parse_input('fact: (topof ?disk '+sl[2]+')'))
        if not answer: # there is no disk on the desination peg
            retract_facts.append(parse_input('fact: (empty '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[2]+')'))
        else:
            retract_facts.append(parse_input('fact: (topof '+answer[0]['?disk']+' '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (ondisk '+sl[0]+' '+answer[0]['?disk']+')'))

        answer = self.kb.kb_ask(parse_input('fact: (ondisk '+sl[0]+' ?disk)'))
        if not answer:
            assert_facts.append(parse_input('fact: (empty '+sl[1]+')'))
        else:
            retract_facts.append(parse_input('fact: (ondisk '+sl[0]+' '+answer[0]['?disk']+')'))
            assert_facts.append(parse_input('fact: (topof '+answer[0]['?disk']+' '+sl[1]+')'))
                
        for fact in retract_facts:
            self.kb.kb_retract(fact)
        for fact in assert_facts:
            self.kb.kb_assert(fact)
    

    
    

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        
        ### Student code goes here
        tuples = ([-1 for _ in range(3)], [-1 for _ in range(3)], [-1 for _ in range(3)])
        listOfBindings = self.kb.kb_ask(parse_input('fact:  (on ?tile ?column ?row)'))
        for binding in listOfBindings:
            index = int(binding['?column'][3]) - 1

            if str(binding['?tile'])!= "empty":

                tuples[int(binding['?row'][3])-1][index] = int(binding['?tile'][4])
            else:

                tuples[int(binding['?row'][3]) - 1][index] = -1



        return tuple(tuple(e) for e in tuples)
        

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        retract_facts = []
        assert_facts = []

        sl = list(map(lambda x: str(x), movable_statement.terms))
        retract_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[1]+' '+sl[2]+')'))
        retract_facts.append(parse_input('fact: (on empty '+sl[3]+' '+sl[4]+')'))
        assert_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[3]+' '+sl[4]+')'))
        assert_facts.append(parse_input('fact: (on empty '+sl[1]+' '+sl[2]+')'))

        for fact in retract_facts:
            self.kb.kb_retract(fact)
        for fact in assert_facts:
            self.kb.kb_assert(fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
