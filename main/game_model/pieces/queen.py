# game_model/pieces/queen.py
from .piece import Piece

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'Q', position)

    def possible_moves(self, board):
        moves = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for d in directions:
            for i in range(1, 8):
                new_pos = (self.position[0] + d[0] * i, self.position[1] + d[1] * i)
                if board.is_valid_position(new_pos):
                    if board.is_empty(new_pos):
                        moves.append(new_pos)
                    elif board.piece_at(new_pos).color != self.color:
                        moves.append(new_pos)
                        break
                    else:
                        break
                else:
                    break
        return moves

