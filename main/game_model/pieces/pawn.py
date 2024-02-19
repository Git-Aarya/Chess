# game_model/pieces/pawn.py

from .piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'P', position)

    def possible_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        one_step_forward = (self.position[0] + direction, self.position[1])

        # Move one step forward
        if board.is_empty(one_step_forward):
            moves.append((self.position, one_step_forward))
            # If the pawn is at the starting position, it can move two steps
            if self.position[0] == start_row:
                two_steps_forward = (self.position[0] + 2 * direction, self.position[1])
                if board.is_empty(two_steps_forward):
                    moves.append((self.position, two_steps_forward))

        # Capturing moves
        capture_moves = [(self.position[0] + direction, self.position[1] + offset) for offset in (-1, 1)]
        for end_pos in capture_moves:
            if board.is_valid_position(end_pos) and not board.is_empty(end_pos) and board.piece_at(
                    end_pos).color != self.color:
                moves.append((self.position, end_pos))

        return moves
