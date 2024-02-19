# game_model/pieces/pawn.py

from .piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'P', position)

    def possible_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1  # White pawns move up (-1), black pawns move down (+1)
        start_row = 6 if self.color == 'white' else 1  # Starting row for white and black pawns
        one_step_forward = (self.position[0] + direction, self.position[1])

        # Move one step forward
        if board.is_empty(one_step_forward):
            moves.append(one_step_forward)
            # If the pawn is at the starting position, it can move two steps
            if self.position[0] == start_row:
                two_steps_forward = (self.position[0] + 2 * direction, self.position[1])
                if board.is_empty(two_steps_forward):
                    moves.append(two_steps_forward)

        # Capturing moves
        capture_moves = [(self.position[0] + direction, self.position[1] + offset) for offset in (-1, 1)]
        for move in capture_moves:
            if board.is_valid_position(move) and not board.is_empty(move) and board.piece_at(move).color != self.color:
                moves.append(move)

        return moves
