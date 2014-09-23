from SgfParser import *
from Board import *

class SgfLoader():
    
    @staticmethod
    def loadData(filenames, format, library):
        ''' Parse the SGF files given by filenames and set up the data
        in the format for our neural network. '''
        assert library in ("pybrain", "theano")
        assert format in ("format1, format2, liberty1")
        
        data = ([], [])
        for filename in filenames:
            try:
                file_data = SgfLoader._loadData(filename, format, library)
            except Exception as e:
                print("In SGF file " + str(filename))
                raise
            data[0].extend(file_data[0])
            data[1].extend(file_data[1])
        data = (np.array(data[0], dtype="int32"), np.array(data[1], dtype="int32"))
        return data
        
    @staticmethod       
    def _loadData(filename, format, library):
        try:
            tokens = SgfParser.tokenizeSgfFile(filename)[1:]
            board = SgfParser.parseSgfHeader(tokens[0], filename)
        
            game_tokens = tokens[1:]
            x_set = []
            y_set = []

            for token_index, token in enumerate(game_tokens):
                intersection = SgfParser.parseSgfToken(token, 19)
                reverse = token_index % 2 != 0
                if format == "format1":
                    x_set.append(board.toArrayFormat1(reverse))
                elif format == "format2":
                    x_set.append(board.toArrayFormat2(reverse))
                elif format == "liberty1":
                    x_set.append(board.toLibertyArray(reverse))
                
                if library == "pybrain":
                    y_set.append(intersection.toFormattedArray(19, reverse))
                elif library == "theano":
                    y_set.append(intersection.toIntegerResult(19, reverse))
                board.applyIntersections([intersection])
        except SgfParsingError as e:
            logging.warning("SgfParsingError occurred for " + str(filename) + ": " + str(e))
            return ([], [])
        return (x_set, y_set)
    