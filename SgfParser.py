from Board import *
from Intersection import *
from StoneColor import *

class SgfParser:
    
    @staticmethod
    def parseSgf(filename):
        '''Probably the most useful method, takes in an SGF and returns
        a Board object representing that SGF '''
        return SgfParser.parseTokenizedSgf(SgfParser.tokenizeSgfFile(filename))
    
    @staticmethod
    def tokenizeSgfFile(filename):
        file = open(filename, 'r')
        #TEST: Windows newlines
        tokens = file.read().replace('\r','').replace('\n','').replace(' ','').split(';')
        file.close()
        return tokens
    
    @staticmethod
    def parseTokenizedSgf(tokens):
        header = tokens[:2]
        game = tokens[2:-1]
        SgfParser.parseTokenizedSgfHeader(header) # incomplete
        return SgfParser.parseTokenizedSgfBody(game)
    
    @staticmethod
    def parseTokenizedSgfHeader(headerTokens):
        ''' Not implemented yet; does nothing'''
        return
    
    @staticmethod
    def parseTokenizedSgfBody(bodyTokens, startingBoard=Board(19)):
        ''' Apply all of the body tokens to the given starting board. If no
        starting board is given, applies the body tokens to anempty 19x19
        board. Mutates startingBoard to be the same as return value.'''
        startingBoard.applyIntersections(
            [SgfParser.parseSgfToken(token) for token in bodyTokens])
        return startingBoard
    
    @staticmethod
    def parseSgfToken(token):
        ''' Takes in a single SGF token and returns an Intersection object
        representing that token.
        '''   
        if (len(token) > 5):
            SgfParser.raiseInvalidSgf(token)
        
        if token[0] == 'B':
            stoneColor = StoneColor.BLACK
        elif token[0] == 'W':
            stoneColor = StoneColor.WHITE
        else:
            SgfParser.raiseInvalidSgf(token)
        
        if token[1] != '[':
            SgfParser.raiseInvalidSgf(token)
        
        if token[2] == ']':
            coordinate = [-1, -1]
        else:
            coordinate = [ord(token[3]) - ord('a'), ord(token[2]) - ord('a')]
        
        return Intersection(coordinate, stoneColor)
        
    @staticmethod        
    def raiseInvalidSgf(token):
        raise ValueError("Error occurred in SGF Parsing for token: " + token)