class Intersection:
    # coordinate is a 2d 0-based tuple.
    # For example, [0, 0] refers to the top-left 1-1 point.
    # [0, 1] refers to the first row, second column.
    # [-1, -1] is a pseudo-intersection used to represent a pass. Call isPass()
    # to check for this property.
    # stoneColor's values are defined in StoneColor.py
    def __init__(self, coordinate, stoneColor):
        self.coordinate = coordinate
        self.stoneColor = stoneColor
    
    def getCoordinate(self):
        return self.coordinate
    
    def isPass(self):
        return self.coordinate == [-1, -1]
    
    @staticmethod
    def getPassCoordinate():
        return [-1, -1]
    
    def getStoneColor(self):
        return self.stoneColor
    
    def toFormattedArray(self, board_size, reverseColor=False):
        ''' Return a board_size array of all zeros except with stoneColor
        stored in the corresponding place in the array that this
        Intersection object refers to.'''
        mult = -1 if reverseColor else 1
        if self.isPass():
            return [[0] for i in range(board_size**2)]
        else:
            location = self.coordinate[0]*board_size + self.coordinate[1]
            return [[0] for i in range(location)] + [[self.stoneColor*mult]] \
                + [[0] for i in range(location+1, board_size**2)]
    
    