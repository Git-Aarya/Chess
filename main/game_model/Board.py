# game_model/Board.py
from .pieces import King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for col in range(8):
            self.board[1][col] = Pawn('black', (1, col))
            self.board[6][col] = Pawn('white', (6, col))

        # Place other pieces on the back rank
        for col, PieceClass in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            self.board[0][col] = PieceClass('black', (0, col))
            self.board[7][col] = PieceClass('white', (7, col))

    def is_empty(self, position):
        row, col = position
        return self.is_valid_position(position) and self.board[row][col] is None

    @staticmethod
    def is_valid_position(position):
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    def piece_at(self, position):
        row, col = position
        if not self.is_valid_position(position):
            return None
        return self.board[row][col]

    def move_piece(self, start_pos, end_pos):
        # Validate positions
        if not self.is_valid_position(start_pos) or not self.is_valid_position(end_pos):
            raise ValueError("Positions out of bounds")

        # Get the piece to move
        piece = self.piece_at(start_pos)
        if piece is None:
            raise ValueError("No piece at start position")

        # Optionally, handle captures
        target_piece = self.piece_at(end_pos)
        if target_piece is not None and target_piece.color != piece.color:
            # Capture logic: for now, simply remove the target piece
            print(f"{piece} captures {target_piece} at {end_pos}")
        elif target_piece is not None:
            raise ValueError("Cannot capture your own piece")

        # Move the piece
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None

        # Update the piece's position
        piece.position = end_pos

    def get_all_possible_moves(self, color):
        moves = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    moves.extend(piece.possible_moves(self))
        return moves

    def is_in_check(self, color):
        king_position = None

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            return False

        opponent_color = 'black' if color == 'white' else 'white'

        for move in self.get_all_possible_moves(opponent_color):
            if move == king_position:
                return True

        return False

