# game_model/pieces/king.py
from .piece import Piece

from .piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'K', position)

    def possible_moves(self, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            new_pos = (self.position[0] + d[0], self.position[1] + d[1])
            if board.is_valid_position(new_pos) and \
                    (board.is_empty(new_pos) or board.piece_at(new_pos).color != self.color):
                moves.append((self.position, new_pos))
        return moves

