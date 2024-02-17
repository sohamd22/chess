from piece import Piece

EMPTY = None

class Board:
    def __init__(self):
        self.state = [
            [Piece('R', 1, [0, 0]), Piece('N', 1, [0, 1]), Piece('B', 1, [0, 2]), Piece('Q', 1, [0, 3]), Piece('K', 1, [0, 4]), Piece('B', 1, [0, 5]), Piece('N', 1, [0, 6]), Piece('R', 1, [0, 7])],
            [Piece('P', 1, [1, 0]), Piece('P', 1, [1, 1]), Piece('P', 1, [1, 2]), Piece('P', 1, [1, 3]), Piece('P', 1, [1, 4]), Piece('P', 1, [1, 5]), Piece('P', 1, [1, 6]), Piece('P', 1, [1, 7])],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [Piece('P', -1, [6, 0]), Piece('P', -1, [6, 1]), Piece('P', -1, [6, 2]), Piece('P', -1, [6, 3]), Piece('P', -1, [6, 4]), Piece('P', -1, [6, 5]), Piece('P', -1, [6, 6]), Piece('P', -1, [6, 7])],
            [Piece('R', -1, [7, 0]), Piece('N', -1, [7, 1]), Piece('B', -1, [7, 2]), Piece('Q', -1, [7, 3]), Piece('K', -1, [7, 4]), Piece('B', -1, [7, 5]), Piece('N', -1, [7, 6]), Piece('R', -1, [7, 7])]
            ]

board = Board()
print(board.state[0][1].getPositions(board.state))