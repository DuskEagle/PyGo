from SgfLoader import *
from SgfParser import *
import numpy as np
import unittest

class SgfUtilTester(unittest.TestCase):
    
    basicSgf1 = 'basicSgf1'
    
    def testParseMoveTokenTopLeftFourFour(self):
        intersection = SgfParser.parseSgfToken("B[dd]")
        self.assertTrue(intersection.getCoordinate() == [3, 3])
        self.assertTrue(intersection.getStoneColor() == StoneColor.BLACK)
        validation = [0 for i in range(60)] + [1] + [0 for i in range(61, 361)]
        self.assertTrue(np.array_equal(intersection.toArray(19), validation))
        
    def testParseMoveBottomRightOneTwo(self):
        intersection = SgfParser.parseSgfToken("W[sr]")
        self.assertTrue(intersection.getCoordinate() == [17, 18])
        self.assertTrue(intersection.getStoneColor() == StoneColor.WHITE)
    
    def testParseMoveBlackPass(self):
        intersection = SgfParser.parseSgfToken("B[]")
        self.assertTrue(intersection.getCoordinate() == [-1, -1])
        self.assertTrue(intersection.getStoneColor() == StoneColor.BLACK)
        board = Board(9)
        self.assertTrue(board.toSlDiagram() == Board(9).toSlDiagram())
        self.assertTrue(np.array_equal(intersection.toArray(9), [0 for i in range (81)]))
        
    def testFileTokenizer(self):
        result = SgfParser.tokenizeSgfFile(self.basicSgf1 + '.sgf')
        self.assertTrue(result == ['(', 'FF[4]', 'B[pd]', 'W[cp]', 'B[dc]', 'B[]', 'W[]', ')'])
    
    def testCreateBoardFromSgf1(self):
        board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        testFile = open(self.basicSgf1 + '.sl')
        correctOutput = testFile.read().rstrip('\n')
        testFile.close()
        self.assertTrue(correctOutput == board.toSlDiagram().rstrip('\n'))
        self.assertTrue(board.getMoveNumber() == 5)
    
    def testToNumpyArray(self):
        board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        actual = board.toNumpyArray()
        validation = np.array([0 for i in range(41)] + [1] \
            + [0 for i in range(30)] + [1] \
            + [0 for i in range(214)] + [-1] + [0 for i in range(73)])
        self.assertTrue(np.array_equal(actual, validation))
    
    def testSgfLoader(self):
        board = SgfParser.parseSgf(self.basicSgf1 + '.sgf')
        data = SgfLoader.loadData([self.basicSgf1 + '.sgf'])
        self.assertTrue(np.array_equal(data[3][0], board.toNumpyArray()))
    
def main():
    unittest.main()

if __name__ == '__main__':
    main()