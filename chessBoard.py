from pieces import *
from collections import defaultdict
import copy

SIZE = 8

DEPTH = 3

WHITE_ROOKS = [Rook(1, 0, 0), Rook(1, 0, (SIZE - 1))]
BLACK_ROOKS = [Rook(-1, (SIZE - 1), 0), Rook(-1, (SIZE - 1), (SIZE - 1))]

WHITE_KNIGHTS = [Knight(1, 0, 1), Knight(1, 0, (SIZE - 1) - 1)]
BLACK_KNIGHTS = [Knight(-1, (SIZE - 1), 1), Knight(-1, (SIZE - 1), (SIZE - 1) - 1)]

WHITE_BISHOPS = [Bishop(1, 0, 2), Bishop(1, 0, (SIZE - 1) - 2)]
BLACK_BISHOPS = [Bishop(-1, (SIZE - 1), 2), Bishop(-1, (SIZE - 1), (SIZE - 1) - 2)]

WHITE_QUEEN = Queen(1, 0, 4)
BLACK_QUEEN = Queen(-1, (SIZE - 1), 4)

WHITE_KING = King(1, 0, (SIZE - 1) - 4)
BLACK_KING = King(-1, (SIZE - 1), (SIZE - 1) - 4)

WHITE_PAWNS = [Pawn(1, 1, i) for i in range(SIZE)]
BLACK_PAWNS = [Pawn(-1, (SIZE - 1) - 1, i) for i in range(SIZE)]


class ChessBoard:
    def __init__(self):
        self.size = SIZE        
        self.player = 1

        self.check = 0

        self.pieces = {1: [], -1: []}
        self.pieces[1].extend([WHITE_KING] + WHITE_ROOKS + WHITE_KNIGHTS + WHITE_BISHOPS + [WHITE_QUEEN] + WHITE_PAWNS)
        self.pieces[-1].extend([BLACK_KING] + BLACK_ROOKS + BLACK_KNIGHTS + BLACK_BISHOPS + [BLACK_QUEEN] + BLACK_PAWNS)

        self.board = [[None for _ in range(SIZE)] for _ in range(SIZE)]
        for piece in self.pieces[1] + self.pieces[-1]:
            self.board[piece.position[0]][piece.position[1]] = piece

        self.visibilitySquares = defaultdict(list)
        for piece in self.pieces[1] + self.pieces[-1]:
            for (row, col) in piece.getVisibility(self.board):
                self.visibilitySquares[(row, col)].append(piece.position)

    def actions(self):
        actions = []
        for piece in self.pieces[self.player]:
            for (row, col) in piece.getVisibility(self.board):
                actions.append((piece.position, (row, col)))
        return actions

    def result(self, oldPosition, newPosition):
        newBoard = copy.deepcopy(self)

        piece = newBoard.board[oldPosition[0]][oldPosition[1]]
        
        if(not(piece) or oldPosition not in newBoard.visibilitySquares[newPosition] or piece.color != newBoard.player):            
            return None

        capturedPiece = newBoard.board[newPosition[0]][newPosition[1]]

        piece.position = newPosition
        newBoard.board[oldPosition[0]][oldPosition[1]] = None
        newBoard.board[newPosition[0]][newPosition[1]] = piece
        
        if(capturedPiece):
            newBoard.pieces[-newBoard.player].remove(capturedPiece)
        
        if(piece.notation.upper() == "P"):
            piece.range = 1

            if(piece.color == -1 and piece.position[0] == 0 or piece.color == 1 and piece.position[0] == (SIZE - 1)):
                newBoard.board[piece.position[0]][piece.position[1]] = Queen(piece.color, piece.position[0], piece.position[1])
        elif(piece.notation.upper() == "K" or piece.notation.upper() == "R"):
            piece.moved = True

        newBoard.visibilitySquares = defaultdict(list)
        for piece in newBoard.pieces[1] + newBoard.pieces[-1]:
            for (row, col) in piece.getVisibility(newBoard.board):
                newBoard.visibilitySquares[(row, col)].append(piece.position)

        if(len(newBoard.visibilitySquares[newBoard.pieces[newBoard.player][0].position])):
            return None
        if(len(newBoard.visibilitySquares[newBoard.pieces[-newBoard.player][0].position])):
            newBoard.check = -newBoard.player
        else:
            newBoard.check = 0
        newBoard.player = -newBoard.player
        return newBoard
    
    def winner(self):
        if(not(self.check)):
            return None
        if(self.terminal()):
            return -self.check
        return None

    def terminal(self):
        found = False
        for piece in self.pieces[-1] + self.pieces[1]:
            for (row, col) in piece.getVisibility(self.board):
                if(self.result(piece.position, (row, col))):
                    found = True
                    break
        if(not(found)):
            return True

    def utility(self):
        winner = self.winner()
        if(winner):
            return winner * 1000000
        if(self.terminal()):
            return 0

        value = 0
        for piece in self.pieces[-1] + self.pieces[1]:
            value += piece.color * 50 * piece.value
        for square in self.visibilitySquares:
            for (row, col) in self.visibilitySquares[square]:
                piece = self.board[row][col]
                if(piece.notation.upper() == "K"):
                    value -= piece.color
                else:
                    value += piece.color
        value += -self.check * 30
        return value
        
    def minimax(self):
        if(self.player == 1):
            return self.maximize(self, 1, -1000000, 1000000)[1]
        return self.minimize(self, 1, -1000000, 1000000)[1]

    def maximize(self, board, currentDepth, alpha, beta):
        if(board.terminal() or currentDepth == DEPTH):
            return [board.utility(), None]

        actionSet = board.actions()
        currentMaximum = [-1000000, None]
        for action in actionSet:
            result = board.result(action[0], action[1])
            if(result):
                bestPossibility = board.minimize(result, currentDepth + 1, alpha, beta)
                if(bestPossibility[0] > currentMaximum[0]):
                    alpha = max(alpha, bestPossibility[0])
                    currentMaximum[0] = bestPossibility[0]
                    currentMaximum[1] = action
                if(currentMaximum[0] == 1000000 or beta <= alpha):
                    break
        return currentMaximum
    
    def minimize(self, board, currentDepth, alpha, beta):
        if(board.terminal() or currentDepth == DEPTH):
            return [board.utility(), None]

        actionSet = board.actions()
        currentMinimum = [1000000, None]
        for action in actionSet:
            result = board.result(action[0], action[1])
            if(result):
                bestPossibility = board.maximize(result, currentDepth + 1, alpha, beta)
                if(bestPossibility[0] < currentMinimum[0]):
                    beta = min(beta, bestPossibility[0])
                    if(beta <= alpha):
                        break
                    currentMinimum[0] = bestPossibility[0]
                    currentMinimum[1] = action
                if(currentMinimum[0] == -1000000 or beta <= alpha):
                    break
        return currentMinimum