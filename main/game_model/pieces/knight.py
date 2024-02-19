# game_model/pieces/knight.py

from .piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'N', position)

    def possible_moves(self, board):
        moves = []
        move_offsets = [
            (-2, -1), (-2, +1),
            (-1, -2), (-1, +2),
            (+1, -2), (+1, +2),
            (+2, -1), (+2, +1)
        ]
        for offset in move_offsets:
            new_row = self.position[0] + offset[0]
            new_col = self.position[1] + offset[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:  # Check if move is within board bounds
                moves.append((new_row, new_col))
        return moves
