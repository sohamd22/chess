import math

EMPTY = None

class Piece:
    def __init__(self, type: str, color: int, position: list[int]):
        self.type = type
        self.position = position
        self.color = color
        self.visibility = []

        match self.type:
            # King
            case "K":
                self.value = float("inf") * self.color
                self.maxMove = 1
                self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] # [Up, Right, Down, Left]

                # Only for King
                self.inCheck = [False, ""]
                self.canCastle = [True, True] # [With Left Rook, With Right Rook]
            
            # Queen
            case "Q":
                self.value = 9 * 1  * self.color
                self.maxMove = 7
                self.directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] # [Up, UpRight, Right, RightDown, Down, DownLeft, Left, LeftUp]
            
            # Rook
            case "R":
                self.value = 5 * self.color
                self.maxMove = 7
                self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] # [Up, Right, Down, Left]
            
            # Bishop
            case "B":
                self.value = 3 * self.color
                self.maxMove = 7
                self.directions = [(1, 1), (-1, 1), (-1, -1), (1, -1)] # [UpRight, RightDown, DownLeft, LeftUp]
            
            # Knight
            case "N":
                self.value = 3 * self.color
                self.maxMove = 1
                self.directions = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)] # Different L positions

            # Pawn
            case "P":
                self.value = self.color
                self.maxMove = 2 # Initially can move 2
                self.directions = [(self.color, 0)] # WUp/BDown

                for direction in self.directions:
                    row, col = self.position[0] + direction[0] * self.maxMove, self.position[1] + direction[1] * self.maxMove
                    if(min(row, col) < 0 or max(row, col) > 7):
                        continue
                    self.visibility.append((row, col))
                
                # Only for Pawn
                self.captureDirections = [(self.color, 1), (self.color, -1)] # W[UpRight, UpLeft], B[DownRight, DownLeft]
        
        
        for direction in self.directions:
            row, col = self.position[0] + direction[0], self.position[1] + direction[1]
            if(min(row, col) < 0 or max(row, col) > 7):
                continue
            self.visibility.append((row, col))    

    def getPositions(self, board: list[list["Piece"]])-> list[str]:
        possibilities = []

        for row, col in self.visibility:
            if(board[row][col] == EMPTY):
                possibilities.append((self.type if(self.color == 1) else self.type.lower()) + chr(97 + row) + str(col + 1))
            elif((self.type != "P" or not(col == 0)) and board[row][col].color == -self.color):
                possibilities.append((self.type if(self.color == 1) else self.type.lower()) + self.type + 'x' + chr(97 + row) + str(col + 1))


        # match self.type:
        #      # King
        #     case "K":
        #         for direction in self.directions:
        #             row, col = self.position[0] + direction[0], self.position[1] + direction[1]
        #             if(board[row][col] == EMPTY):
        #                 possibilities.append(self.type + chr(97 + row) + (col + 1))
        #             elif(board[row][col].color == -self.color):
        #                 possibilities.append(self.type + 'x' + chr(97 + row)  + (col + 1))

        #         # Castling
        #         if(self.canCastle[0]):
        #             possibilities.append("O-O-O" if self.color == 1 else "O-O")
        #         elif(self.canCastle[1]):
        #             possibilities.append("O-O" if self.color == 1 else "O-O-O")
            
        #     # Queen, Rook, Bishop, Knight, Pawn
        #     case "Q" | "R" | "B" | "N" | "P":
        #         for direction in self.directions:
        #             for distance in range(1, self.maxMove + 1):
        #                 row, col = self.position[0] + direction[0] * distance, self.position[1] + direction[1] * distance
        #                 if(board[row][col] == EMPTY):
        #                     possibilities.append(self.type + chr(97 + row) + (col + 1))
        #                 elif(self.type != "P" and board[row][col].color == -self.color):
        #                     possibilities.append(self.type + 'x' + chr(97 + row)  + (col + 1))
        #         if(self.type == "P"):
        #             for captureDirection in self.captureDirections:
        #                 row, col = self.position[0] + captureDirection[0], self.position[1] + captureDirection[1]
        #                 if(board[row][col] == EMPTY):
        #                     continue
        #                 if(board[row][col].color == -self.color):
        #                     possibilities.append(self.type + 'x' + chr(97 + row) + (col + 1))                
        
        return possibilities       
    
    def visibilityAtPosition(self, row, col, board: list[list["Piece"]]) -> list[tuple]:
        visibility = [(row, col)]

        for direction in self.directions:
            for distance in range(1, self.maxMove + 1):
                newRow, newCol = row + direction[0] * distance, col + direction[1] * distance
                visibility.append((newRow, newCol))
                if(board[newRow][newCol] != EMPTY):
                    break
        
        if(self.type == "P"):
            for captureDirection in self.captureDirections:
                newRow, newCol = row + captureDirection[0], col + captureDirection[1]
                visibility.append((row, col))

    
    