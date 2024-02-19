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
        for d in move_offsets:
            new_pos = (self.position[0] + d[0], self.position[1] + d[1])
            if board.is_valid_position(new_pos) and \
                    (board.is_empty(new_pos) or board.piece_at(new_pos).color != self.color):
                moves.append((self.position, new_pos))
        return moves
