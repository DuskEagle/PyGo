class StoneColor:
    NONE = 0;
    BLACK = 1;
    WHITE = -1;
    
    @staticmethod
    def opposite(color):
        if color == StoneColor.NONE:
            return StoneColor.NONE
        elif color == StoneColor.BLACK:
            return StoneColor.WHITE
        elif color == StoneColor.WHITE:
            return StoneColor.BLACK
        else:
            raise ValueError(str(color) + " is not a valid stone color.")