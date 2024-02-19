import pygame

from main.game_model.Board import Board
from main.game_model.pieces import King
class game_main:
    def __init__(self):
        pygame.init()
        self.board = Board()
        self.screen = pygame.display.set_mode((800, 800))  # Adjust as needed
        self.current_turn = 'white'
        self.selected_piece = None
        self.running = True
        self.game_over = False

    def draw(self):
        # Draw the board
        for row in range(8):
            for col in range(8):
                color = (119, 149, 86) if (row + col) % 2 == 0 else (235, 236, 208)
                pygame.draw.rect(self.screen, color, pygame.Rect(col * 100, row * 100, 100, 100))

        # Highlight squares based on possible moves
        possible_moves = self.board.get_all_possible_moves(self.current_turn)
        for move in possible_moves:
            pygame.draw.rect(self.screen, (0, 255, 255), pygame.Rect(move[1] * 100, move[0] * 100, 100, 100), 5)

        # Draw the pieces
        for row in range(8):
            for col in range(8):
                piece = self.board.piece_at((row, col))
                if piece:
                    image = pygame.image.load(f'images/{piece}.png')
                    image_rect = image.get_rect()
                    centered_x = col * 100 + (100 - image_rect.width) // 2
                    centered_y = row * 100 + (100 - image_rect.height) // 2
                    self.screen.blit(image, (centered_x, centered_y))

    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.draw()
            pygame.display.flip()

            # Debugging: Print the check and checkmate status
            if self.board.is_in_check(self.current_turn):
                print(f"{self.current_turn} is in check.")
                self.game_over = False

            if self.is_checkmate():
                print(f"Checkmate detected for {self.current_turn}. Game over.")
                self.game_over = True

            elif self.is_draw():
                print("Draw detected. Game over.")
                self.game_over = True
            else:
                # Continue with the game logic
                self.game_over = False

            if self.game_over:
                self.running = False
                # Display the result more clearly or pause for input
                print("Game over. Press any key to exit.")
                pygame.event.wait()

            pygame.time.delay(100)

    def handle_mouse_click(self, position):
        col = position[0] // 100
        row = position[1] // 100
        selected_pos = (row, col)

        if self.selected_piece:
            success = self.make_move(self.selected_piece, selected_pos)
            if success:
                self.selected_piece = None
            else:
                # illegal move or trying to select another piece
                self.selected_piece = selected_pos if self.board.piece_at(selected_pos) else None
        else:
            if self.board.piece_at(selected_pos) and self.board.piece_at(selected_pos).color == self.current_turn:
                self.selected_piece = selected_pos

    def switch_turns(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def make_move(self, start_pos, end_pos):
        if not self.board.is_valid_position(start_pos) or not self.board.is_valid_position(end_pos):
            print("Invalid positions.")
            return False

        piece = self.board.piece_at(start_pos)
        if piece is None or piece.color != self.current_turn:
            print("No piece at the start position or not your turn.")
            return False

        if end_pos in piece.possible_moves(self.board):
            self.board.move_piece(start_pos, end_pos)
            if self.board.is_in_check(self.current_turn):
                print("Move puts you in check, try another move.")
                return False
            self.switch_turns()
            return True
        else:
            print("Illegal move for the piece.")
            return False

    def is_checkmate(self):
        if not self.board.is_in_check(self.current_turn):
            return False

        # Get all possible moves for the current player
        all_moves = self.board.get_all_possible_moves(self.current_turn)

        # Try each move to see if it can escape check
        for start_pos, end_pos in all_moves:
            # Simulate the move
            piece = self.board.piece_at(start_pos)
            captured_piece = self.board.piece_at(end_pos)
            self.board.move_piece(start_pos, end_pos)

            # Check if still in check
            still_in_check = self.board.is_in_check(self.current_turn)

            # Undo the move
            self.board.move_piece(end_pos, start_pos)
            if captured_piece:
                self.board.board[end_pos[0]][end_pos[1]] = captured_piece

            # If found a move that escapes check, not checkmate
            if not still_in_check:
                return False

        # If no moves escape check, it's checkmate
        return True

    def is_draw(self):
        # Check for stalemate: no legal moves but not in check
        if not self.board.get_all_possible_moves(self.current_turn) and not self.board.is_in_check(self.current_turn):
            print("Draw due to stalemate.")
            return True

        # Simplified check for insufficient material: only kings left
        pieces = [piece for row in self.board.board for piece in row if piece is not None]
        if len(pieces) == 2 and all(isinstance(piece, King) for piece in pieces):
            print("Draw due to insufficient material.")
            return True

    @staticmethod
    def main():
        game_instance = game_main()
        game_instance.play()

if __name__ == "__main__":
    game_main.main()
