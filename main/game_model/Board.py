# game_model/Board.py
from main.game_model.pieces import Rook, Knight, Bishop, Queen, King, Pawn


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

    def move_piece(self, start_pos, end_pos, is_simulation=False):
        # Validate positions first
        if not self.is_valid_position(start_pos) or not self.is_valid_position(end_pos):
            raise ValueError("Positions out of bounds")

        # Get the piece at the start position
        moving_piece = self.piece_at(start_pos)
        if moving_piece is None:
            raise ValueError("No piece at start position")

        # Check if there's a piece at the end position (potential capture)
        captured_piece = self.piece_at(end_pos)

        # If it's not a simulation, log the capture
        if captured_piece and not is_simulation:
            print(f"{moving_piece} captures {captured_piece} at {end_pos}")


        # Execute the move
        self.board[end_pos[0]][end_pos[1]] = moving_piece
        self.board[start_pos[0]][start_pos[1]] = None

        # Update the moving piece's position attribute
        moving_piece.position = end_pos

        # Pawn Promotion
        if isinstance(moving_piece, Pawn) and (end_pos[0] == 0 or end_pos[0] == 7):
            self.board[end_pos[0]][end_pos[1]] = Queen(moving_piece.color, end_pos)

    def get_all_possible_moves(self, color):
        moves = []
        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    moves.extend(piece.possible_moves(self))
        return moves

    def is_in_check(self, color):
        king_position = None

        # Find the king's position
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

        # Check if any move attacks the king's position
        for start_pos, end_pos in self.get_all_possible_moves(opponent_color):
            if end_pos == king_position:
                return True

        return False

