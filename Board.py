from StoneColor import *
import numpy as np

class Board:
    # board is an n*n array of StoneColors.
    def __init__(self, size):
        self.board = []
        self.board_size = size
        self.move_number = 0
        for i in range(size):
            self.board.append([])
            for j in range(size):
                self.board[i].append(StoneColor.NONE)
    
    def getBoard(self):
        return self.board
    
    def toFormattedArray(self, reverseColor=False):
        mult = -1 if reverseColor else 1
        l = []
        for row in self.board:
            for col in row:
                l.append([col*mult])
        return l
    
    def applyIntersections(self, intersections):
        for intersection in intersections:
            self.move_number += 1
            if not intersection.isPass():
                coordinate = intersection.getCoordinate()
                self.board[coordinate[0]][coordinate[1]] = intersection.getStoneColor()
    
    def getMoveNumber(self):
        return self.move_number
    
    def toSlDiagram(self):
        str_list = ["$$ \n"]
        
        str_list.append("$$ ")
        str_list.append("-"*(self.board_size*2+3))
        str_list.append("\n")
        
        for row_index, row in enumerate(range(self.board_size)):
            str_list.append("$$ | ")
            for col_index, col in enumerate(range(self.board_size)):
                if self.board[row][col] == StoneColor.BLACK:
                    str_list.append("X ")
                elif self.board[row][col] == StoneColor.WHITE:
                    str_list.append("O ")
                else:
                    if row_index in [3, 9, 15] and col_index in [3, 9, 15]:
                        str_list.append(", ")
                    else:
                        str_list.append(". ")
            str_list.append("|\n")
         
        str_list.append("$$ ")
        str_list.append("-"*(self.board_size*2+3))
        str_list.append("\n")
    
        return ''.join([s for s in str_list])
    
    def __str__(self):
        return self.toSlDiagram()
