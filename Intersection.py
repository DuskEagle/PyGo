import numpy as np

class Intersection:
    # coordinate is a 2d 0-based tuple.
    # For example, [0, 0] refers to the top-left 1-1 point.
    # [0, 1] refers to the first row, second column.
    # [-1, -1] is a pseudo-intersection used to represent a pass. Call isPass()
    # to check for this property.
    # stone_color's values are defined in StoneColor.py
    def __init__(self, coordinate, stone_color):
        self.coordinate = coordinate
        self.stone_color = stone_color
    
    def getCoordinates(self):
        return self.coordinate
    
    def isPass(self):
        return self.coordinate == [-1, -1]
    
    @staticmethod
    def getPassCoordinate():
        return [-1, -1]
    
    def getStoneColor(self):
        return self.stone_color
    
    def setStoneColor(self, color):
        self.stone_color = color
    
    def toFormattedArray(self, board_size, reverseColor=False):
        ''' Return a board_size array of all zeros except with stone_color
        stored in the corresponding place in the array that this
        Intersection object refers to.'''
        mult = -1 if reverseColor else 1
        if self.isPass():
            result = [0 for i in range(board_size**2)]
        else:
            location = self.coordinate[0]*board_size + self.coordinate[1]
            result = [0 for i in range(location)] + [self.stone_color*mult] \
                + [0 for i in range(location+1, board_size**2)]
        return result
    
    def toIntegerResult(self, board_size, reverseColor=False):
        if self.isPass():
            return board_size**2 # One past the end of the board for a pass.
        return np.argmax(self.toFormattedArray(board_size, reverseColor))
    
    