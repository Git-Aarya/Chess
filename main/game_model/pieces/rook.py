# game_model/pieces/rook.py
from .piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'R', position)

    def possible_moves(self, board):
        moves = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for d in directions:
            for i in range(1, 8):
                end_row = self.position[0] + d[0] * i
                end_col = self.position[1] + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = board.piece_at((end_row, end_col))
                    if end_piece is None:
                        moves.append((self.position, (end_row, end_col)))
                    elif end_piece.color != self.color:
                        moves.append((self.position, (end_row, end_col)))
                        break
                    else:
                        break
                else:
                    break
        return moves
