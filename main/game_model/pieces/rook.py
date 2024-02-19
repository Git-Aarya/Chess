# game_model/pieces/rook.py
from .piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'R', position)

    def possible_moves(self, board):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for d in directions:
            for i in range(1, 8):
                end_row = self.position[0] + d[0] * i
                end_col = self.position[1] + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:  # Stay within board bounds
                    end_piece = board[end_row][end_col]
                    if end_piece is None:
                        moves.append((end_row, end_col))  # Empty square is a valid move
                    elif end_piece.color != self.color:
                        moves.append((end_row, end_col))  # Capture the opponent's piece
                        break
                    else:
                        break  # Blocked by a piece of the same color
                else:
                    break  # Off the board
        return moves
