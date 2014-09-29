import logging
import re
from Board import *
from Intersection import *
from StoneColor import *

class SgfParser:
    
    @staticmethod
    def parseSgf(filename):
        """Probably the most useful method, takes in an SGF and returns
        a Board object representing that SGF."""
        return SgfParser.parseTokenizedSgf(SgfParser.tokenizeSgfFile(filename), filename)
            
    
    @staticmethod
    def tokenizeSgfFile(filename):
        file = open(filename, 'r')
        try:
            tokens = SgfParser._sgfSplit(file.read().replace('\n','').replace('\r','').replace(' ',''))
        except UnicodeDecodeError:
            logging.warning("Invalid utf-8 character found in " + str(filename) + "; skipping.")
            raise SgfParsingError
        file.close()
        return tokens
    
    @staticmethod
    def _sgfSplit(string):
        """ Like <String>.split(';'), but only when ';' is not encased between a
        '[ ]' bracket pair. """
        tokens = []
        bracket_count = 0
        run = 0
        for index, char in enumerate(string):
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
            elif char == ';' and bracket_count == 0:
                tokens.append(string[run:index])
                run = index+1
                
            if bracket_count < 0:
                raise SgfParsingError("']' bracket found without an opening '[' bracket.")
        
        if run <= index:
            tokens.append(string[run:])
        return tokens
    
    @staticmethod
    def parseTokenizedSgf(tokens, board_name):
        header = tokens[1]
        game = tokens[2:]
        board = SgfParser.parseSgfHeader(header, board_name)
        return SgfParser.parseTokenizedSgfBody(game, board)
    
    @staticmethod
    def parseSgfHeader(header, filename=None):
        """ Returns a board initialized based on the header information (e.g 
        size, handicap stones). 
        
        filename gets passed through to the Board object that gets returned."""
        
        size_match = re.search('SZ\\[(.+?)\\]', header)
        if size_match:
            try:
                board_size = size_match.group(1)
                board_size = int(board_size)
            except ValueError:
                raise SgfParsingError("Non-integer board size \"" + str(board_size) + \
                    "\" found while parsing SGF file.")
        else:
            board_size = 19
        board = Board(board_size, filename)
        
        starting_black_stones = re.search('AB((?:\\[.+?\\])*)', header)
        if starting_black_stones:
            tokens = starting_black_stones.group(1)
            for i in range(0, len(tokens), 4):
                board.applyIntersections([SgfParser.parseSgfToken('B'+tokens[i:i+4], board_size)])
        starting_white_stones = re.search('AW((?:\\[.+?\\])*)', header)
        if starting_white_stones:
            tokens = starting_white_stones.group(1)
            for i in range(0, len(tokens), 4):
                board.applyIntersections([SgfParser.parseSgfToken('W'+tokens[i:i+4], board_size)])
        
        return board
    
    @staticmethod
    def parseTokenizedSgfBody(bodyTokens, startingBoard=Board(19)):
        ''' Apply all of the body tokens to the given starting board. If no
        starting board is given, applies the body tokens to anempty 19x19
        board. Mutates startingBoard to be the same as return value.'''
        startingBoard.applyIntersections( \
            filter(lambda intersection : intersection != None, \
            [SgfParser.parseSgfToken(token, startingBoard.size) for token in bodyTokens]))
        return startingBoard
    
    @staticmethod
    def parseSgfToken(token, board_size=19):
        ''' Takes in a single SGF token and returns an Intersection object
        representing that token.
        '''
        try:
            if token == ")":
                return None
            if len(token) > 5 and token[5] not in (")", "C"):
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
            elif board_size <= 19 and token[2] == 't' and token[3] == 't': # Part of SGF standard
                coordinate = [-1, -1]
            else:
                coordinate = [ord(token[3]) - ord('a'), ord(token[2]) - ord('a')]
        except IndexError:
            SgfParser.raiseInvalidSgf(token)
        return Intersection(coordinate, stoneColor)
        
    @staticmethod        
    def raiseInvalidSgf(token):
        raise SgfParsingError("Error occurred in SGF Parsing for token: " + token)

class SgfParsingError(RuntimeError):
    pass