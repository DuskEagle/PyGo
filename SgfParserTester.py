from SgfLoader import *
from SgfParser import *
import logging
import numpy as np
import unittest

class SgfUtilTester(unittest.TestCase):
    
    basicSgf1 = 'basicSgf1'
    koSgf = 'ko'
    logging.basicConfig(level=logging.DEBUG)
    
    #def testParseMoveTokenTopLeftFourFour(self):
        #intersection = SgfParser.parseSgfToken('B[dd]')
        #self.assertTrue(intersection.getCoordinates() == [3, 3])
        #self.assertTrue(intersection.getStoneColor() == StoneColor.BLACK)
        #validation = [0 for i in range(60)] + [1] + [0 for i in range(61, 361)]
        #self.assertTrue(np.array_equal(intersection.toFormattedArray(19), validation))
        
    #def testParseMoveBottomRightOneTwo(self):
        #intersection = SgfParser.parseSgfToken('W[sr]')
        #self.assertTrue(intersection.getCoordinates() == [17, 18])
        #self.assertTrue(intersection.getStoneColor() == StoneColor.WHITE)
    
    #def testParseMoveBlackPass(self):
        #intersection = SgfParser.parseSgfToken('B[]')
        #self.assertTrue(intersection.getCoordinates() == [-1, -1])
        #self.assertTrue(intersection.getStoneColor() == StoneColor.BLACK)
        #board = Board(9)
        #self.assertTrue(board.toSlDiagram() == Board(9).toSlDiagram())
        #self.assertTrue(np.array_equal(intersection.toFormattedArray(9), [0 for i in range (81)]))
        
    #def testFileTokenizer(self):
        #result = SgfParser.tokenizeSgfFile(self.basicSgf1 + '.sgf')
        #self.assertTrue(result == ['(', 'FF[4]', 'B[pd]', 'W[cp]', 'B[dc]', 'B[]', 'W[]', ')'])
    
    #def testCreateBoardFromSgf1(self):
        #board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        #testFile = open(self.basicSgf1 + '.sl')
        #correctOutput = testFile.read().rstrip('\n')
        #testFile.close()
        #self.assertTrue(correctOutput == board.toSlDiagram().rstrip('\n'))
        #self.assertTrue(board.getMoveNumber() == 5)
    
    #def testToNumpyArray(self):
        #board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        #actual = board.toFormattedArray()
        #validation = np.array([0 for i in range(41)] + [1] \
            #+ [0 for i in range(30)] + [1] \
            #+ [0 for i in range(214)] + [-1] + [0 for i in range(73)])
        #self.assertTrue(np.array_equal(actual, validation))
    
    #def testSgfLoader(self):
        #board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        #data = SgfLoader.loadData([self.basicSgf1 + '.sgf'])
        #self.assertTrue(np.array_equal(data[3][0], board.toFormattedArray()))
    
    def testLibertyHandling1(self):
        board = SgfParser.parseSgf(self.koSgf + '.sgf')
        self.assertTrue(board.board[4][4] == StoneColor.WHITE)
        self.assertTrue(board.liberty_map[4][4] == 1)
        self.assertTrue(board.board[4][5] == StoneColor.NONE)
        self.assertTrue(board.liberty_map[4][5] == 0)
        self.assertTrue(board.liberty_map[4][6] == 4)
        self.assertTrue(board.liberty_map[4][3] == 3)
     
    def testLibertyHandling2(self):
        board = SgfParser.parseSgf('largeCapture.sgf')

        self.assertTrue(board.board[4][4] == StoneColor.WHITE)
        self.assertTrue(board.liberty_map[4][4] == 4)
        self.assertTrue(board.board[4][5] == StoneColor.NONE)
        self.assertTrue(board.liberty_map[5][5] == 7)
    
    def testLibertyHandling3(self):
        board = SgfParser.parseSgf('ko2.sgf')

        self.assertTrue(board.board[6][0] == StoneColor.NONE)
        self.assertTrue(board.liberty_map[6][0] == 0)
        self.assertTrue(board.board[6][1] == StoneColor.WHITE)
        self.assertTrue(board.liberty_map[6][1] == 1)
        self.assertTrue(board.liberty_map[5][1] == 1)
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()