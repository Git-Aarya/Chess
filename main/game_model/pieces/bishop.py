# game_model/pieces/bishop.py
from .piece import Piece

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'B', position)

    def possible_moves(self, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
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
