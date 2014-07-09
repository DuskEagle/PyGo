from SgfParser import *
from Board import *

class SgfLoader():
    
    @staticmethod
    def loadData(filenames):
        data = []
        for filename in filenames:
            file_data = SgfLoader._loadData(filename) # Still have to put together
            for datum in file_data:
                data.append((datum[0], datum[1]))
        data = np.array(data, dtype=np.float64)
        return data
        
    @staticmethod       
    def _loadData(filename):
        board = Board(19)
        game_tokens = SgfParser.tokenizeSgfFile(filename)[2:-1]
        board_move_pairs = []
        ''' Each element in board_move_pairs: A tuple.
        The first value is a (board size)**2-length array representing a board state.
        The second value is a (board size)-length array representing the correct move
        to play from that board state.'''

        for token_index, token in enumerate(game_tokens):
            intersection = SgfParser.parseSgfToken(token)
            if token_index % 2 == 0:
                board_move_pairs.append((board.toFormattedArray(), intersection.toFormattedArray(19)))
            else:
                board_move_pairs.append((board.toFormattedArray(reverseColor=True), intersection.toFormattedArray(19, reverseColor=True)))
        return board_move_pairs
