SIZE = 8

class Piece:
    def __init__(self, color: int, r: int, c: int) -> None:
        self.color = color
        self.notation = None
        self.value = 1
        self.directions = None
        self.range = 100

        self.position = (r, c)
    
    def getVisibility(self, board: list[list["Piece"]]) -> list:
        visibility = []

        for direction in self.directions:
            for distance in range(1, self.range + 1):
                newRow, newCol = self.position[0] + direction[0] * distance, self.position[1] + direction[1] * distance
                if(min(newRow, newCol) < 0 or max(newRow, newCol) > SIZE - 1):
                    break
                
                if(board[newRow][newCol] != None):
                    if(self.notation.upper() != 'P' and board[newRow][newCol].color == -self.color):
                        visibility.append((newRow, newCol))
                    break
                visibility.append((newRow, newCol))
        
        if(self.notation.upper() == "P"):
            for captureDirection in self.captureDirections:
                newRow, newCol = self.position[0] + captureDirection[0], self.position[1] + captureDirection[1]
                if(min(newRow, newCol) < 0 or max(newRow, newCol) > SIZE - 1):
                    break
                if(board[newRow][newCol] != None and board[newRow][newCol].color == -self.color):
                    visibility.append((newRow, newCol))
        
        return visibility

class King(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(King, self).__init__(color, r, c)
        self.notation = "K" if color == 1 else "k"
        self.value = 1000
        self.directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        self.range = 1
        
        self.moved = False

class Queen(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(Queen, self).__init__(color, r, c)
        self.notation = "Q" if color == 1 else "q"
        self.value = 9
        self.directions = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))

class Rook(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(Rook, self).__init__(color, r, c)
        self.notation = "R" if color == 1 else "r"
        self.value = 5
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

        self.moved = False

class Bishop(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(Bishop, self).__init__(color, r, c)
        self.notation = "B" if color == 1 else "b"
        self.value = 3
        self.directions = ((1, 1), (-1, 1), (-1, -1), (1, -1))

class Knight(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(Knight, self).__init__(color, r, c)
        self.notation = "N" if color == 1 else "n"
        self.value = 3
        self.directions = ((2, 1), (1, 2), (-2, 1), (-1, 2), (2, -1), (1, -2), (-2, -1), (-1, -2))
        self.range = 1

class Pawn(Piece):
    def __init__(self, color: int, r: int, c: int) -> None:
        super(Pawn, self).__init__(color, r, c)
        self.notation = "P" if color == 1 else "p"
        self.directions = ((self.color, 0),)
        self.captureDirections = ((self.color, -1), (self.color, 1))
        self.range = 2

