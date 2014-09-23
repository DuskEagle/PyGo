from StoneColor import *
import logging
import numpy as np

class Board:
    # board is an n*n array of StoneColors.
    def __init__(self, size, name=None):
        self.board = []
        self.liberty_map = []
        self.name = name
        self.size = size
        self.move = 0
        for i in range(size):
            self.board.append([])
            self.liberty_map.append([])
            for j in range(size):
                self.board[i].append(StoneColor.NONE)
                self.liberty_map[i].append(0)
    
    def getBoard(self):
        return self.board
    
    def toArrayFormat1(self, reverse_color=False):
        """
        [1], [0], [0]: Empty
        [0], [1], [0]: Black
        [0], [0], [1]: White
        """
        l = []
        for row in self.board:
            for col in row:
                if col == StoneColor.NONE:
                    l.extend([1, 0, 0])
                elif (not reverse_color and col == StoneColor.BLACK) \
                    or (reverse_color and col == StoneColor.WHITE):
                    l.extend([0, 1, 0])
                else:
                    l.extend([0, 0, 1])
        return l
    
    def toArrayFormat2(self, reverse_color=False):
        """ A (self.size**2)*2 array, where the first self.size**2 elements
        correspond to the locations of the black stones (1 if stone is at that
        spot, 0 otherwise), followed by the next self.size**2 elements doing
        the same for the white stones. """
        arr = []
        for i in range(2):
            if reverse_color:
                color = StoneColor.WHITE if i == 0 else StoneColor.BLACK
            else:
                color = StoneColor.BLACK if i == 0 else StoneColor.WHITE
            for row in range(self.size):
                for col in range(self.size):
                    arr.append(1 if self.board[row][col] == color else 0)
        return arr
    
    def toLibertyArray(self, reverse_color=False):
        """ A (self.size**2)*3*2 array. The first self.size**2 elements map from a board to 1
        if a black group with a piece on that part of the board has 1 liberty,
        or 0 otherwise. The second self.size**2 elements map from a board to a black
        group with 2 liberties, and the third self.size**2 elements for more than 2
        liberties. The next (self.size**2)*2 elements represent the same pattern for the
        white groups """
        arr = []
        for i in range(2):
            if reverse_color:
                color = StoneColor.WHITE if i == 0 else StoneColor.BLACK
            else:
                color = StoneColor.BLACK if i == 0 else StoneColor.WHITE
            for j in range(1,4):
                for row in range(self.size):
                    for col in range(self.size):
                        if j < 3:
                            arr.append(1 if self.board[row][col] == color \
                                and self.liberty_map[row][col] == j else 0)
                        else:
                            arr.append(1 if self.board[row][col] == color \
                                and self.liberty_map[row][col] >= j else 0)
        return arr
    
    def applyIntersections(self, intersections):
        for intersection in intersections:
            self.move += 1
            if not intersection.isPass():
                coordinate = intersection.getCoordinates()
                self.board[coordinate[0]][coordinate[1]] = intersection.getStoneColor()
                self.updateLiberties(intersection)
    
    def updateLiberties(self, focal_intersection, *, _prevent_recursion=False):
        """ Update self.liberty_map with the new liberty count of each group,
        and remove any groups from the board which have no liberties. 
        
        focal_intersection should be an Intersection object representing
        the move just played.
        
        _prevent_recursion should not be set by anything but this function.
        It is used by this function itself to prevent infinite recursion."""
        
        def search (color, starting_coordinates):
            """ Mutates starting_coordinates (will be empty afterward). """
            
            def adjacentCoordinates (coordinates):
                adj = []
                row, col = coordinates[0], coordinates[1]
                if row > 0:
                    adj.append((row-1, col))
                if row < self.size - 1:
                    adj.append((row+1, col))
                if col > 0:
                    adj.append((row, col-1))
                if col < self.size - 1:
                    adj.append((row, col+1))
                return adj
            
            opposite_color_unvisited = []
            group_with_zero_liberties = False
            
            while len(starting_coordinates) > 0:
                start = starting_coordinates.pop()
                while len(starting_coordinates) > 0 and new_liberty_map[start[0]][start[1]] != UNVISITED:
                    start = starting_coordinates.pop()
                
                if len(starting_coordinates) == 0 and new_liberty_map[start[0]][start[1]] not in (UNSEEN, UNVISITED):
                    break
                
                liberties = 0
                group = []
                counted_liberties = set()
                unvisited = [start]
                
                while len(unvisited) > 0:
                    current = unvisited.pop()
                    group.append(current)
                    for row, col in adjacentCoordinates(current):
                        stone_color = self.board[row][col]
                        if stone_color != StoneColor.NONE:
                            if new_liberty_map[row][col] == UNSEEN:
                                if stone_color == color:
                                    new_liberty_map[row][col] = UNVISITED
                                    unvisited.append((row,col))
                                else:
                                    opposite_color_unvisited.append((row,col))
                        elif (row, col) not in counted_liberties:
                            counted_liberties.add((row,col))
                            liberties += 1
                if liberties == 0:
                    group_with_zero_liberties = True
                for row, col in group:
                    new_liberty_map[row][col] = liberties
            
            if len(opposite_color_unvisited) > 0:
                return search (StoneColor.opposite(color), opposite_color_unvisited) or group_with_zero_liberties
            
            return group_with_zero_liberties
                    
        def mergeNewLibertyMap(new_liberty_map):
            for row in range(self.size):
                for col in range(self.size):
                    new_liberties = new_liberty_map[row][col]
                    if new_liberties >= 0:
                        self.liberty_map[row][col] = new_liberties
        
        UNSEEN = -3
        UNVISITED = -2
        VISITED = -1
        # == 0: empty ; > 0: num liberties
        new_liberty_map = [[UNSEEN]*self.size for row in [None for col in range(self.size)]]
        group_with_zero_liberties = False
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] != StoneColor.NONE and new_liberty_map[row][col] == UNSEEN:
                    group_with_zero_liberties = search(self.board[row][col], [(row, col)]) or group_with_zero_liberties
        mergeNewLibertyMap(new_liberty_map)
        
        if group_with_zero_liberties:
            
            if _prevent_recursion:
                raise RuntimeError("Attempted to remove captured groups more than once! Board name: " + str(self.name) + ", move: " + str(self.move) + ", board: " + str(self))
            
            # We'll assume suicide isn't a valid move, so we only have to search
            # for opposite colored stones to remove.
            color_to_remove = StoneColor.opposite(focal_intersection.getStoneColor())
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == color_to_remove and self.liberty_map[row][col] == 0:
                        self.board[row][col] = StoneColor.NONE
                    
            self.updateLiberties(focal_intersection, _prevent_recursion=True) # NOTE: Assumes suicide is impossible.

    def getMoveNumber(self):
        return self.move
    
    def toSlDiagram(self):
        str_list = ["$$ \n"]
        
        str_list.append("$$ ")
        str_list.append("-"*(self.size*2+3))
        str_list.append("\n")
        
        for row_index, row in enumerate(range(self.size)):
            str_list.append("$$ | ")
            for col_index, col in enumerate(range(self.size)):
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
        str_list.append("-"*(self.size*2+3))
        str_list.append("\n")
    
        return ''.join([s for s in str_list])
    
    def __str__(self):
        return self.toSlDiagram()
