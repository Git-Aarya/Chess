import pygame

from main.game_model.Board import Board
from main.game_model.pieces import King, Bishop, Knight


class game_main:
    def __init__(self):
        pygame.init()
        self.board = Board()
        self.screen = pygame.display.set_mode((800, 800))  # Adjust as needed
        self.current_turn = 'white'
        self.selected_piece = None
        self.running = True
        self.game_over = False
        self.game_over = False
        self.is_invisible_mode = False

    def display_start_menu(self):
        menu_running = True

        bg_image = pygame.image.load('bg/bg_image.jpg')
        bg_image = pygame.transform.scale(bg_image, self.screen.get_size())

        bg_color = (3, 37, 76)  # Dark blue background
        text_color = (255, 255, 255)  # White text
        button_color = (85, 45, 10)  # buttons
        hover_color = (45, 21,0)  # hover color
        border_color = (255, 255, 255)  # border color
        font = pygame.font.Font(None, 36)  # Adjust font size as needed

        screen_width, screen_height = self.screen.get_size()
        button_width = 230
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button1_y = screen_height * 0.4
        button2_y = button1_y + button_height + 20

        button1_rect = pygame.Rect(button_x, button1_y, button_width, button_height)
        button2_rect = pygame.Rect(button_x, button2_y, button_width, button_height)

        while menu_running:
            self.screen.blit(bg_image, (0, 0))

            mx, my = pygame.mouse.get_pos()
            button1_hover = button1_rect.collidepoint((mx, my))
            button2_hover = button2_rect.collidepoint((mx, my))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    self.running = False
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_hover:
                        return 'normal'
                    elif button2_hover:
                        return 'invisible'

            # Draw buttons
            pygame.draw.rect(self.screen, border_color, button1_rect, border_radius=10)
            pygame.draw.rect(self.screen, border_color, button2_rect, border_radius=10)
            pygame.draw.rect(self.screen, button_color, button1_rect, border_radius=10)
            pygame.draw.rect(self.screen, button_color, button2_rect, border_radius=10)

            # Draw hover effect
            if button1_hover:
                pygame.draw.rect(self.screen, hover_color, button1_rect, border_radius=10)
            if button2_hover:
                pygame.draw.rect(self.screen, hover_color, button2_rect, border_radius=10)

            # Adjust text rendering to be more centered within the buttons
            text_surface = font.render("Play Normal Chess", True, text_color)
            self.screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2,
                                            button1_y + (button_height - text_surface.get_height()) / 2))
            text_surface = font.render("Play Blind Pieces", True, text_color)
            self.screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2,
                                            button2_y + (button_height - text_surface.get_height()) / 2))

            pygame.display.flip()

    def display_end_menu(self, winning_color):
        menu_running = True

        background_image = pygame.image.load('bg/end_bg.jpg')
        background_image = pygame.transform.scale(background_image, self.screen.get_size())
        text_color = (0, 0, 0)  # White text
        hover_color = (0, 51, 51)  # hover color
        font = pygame.font.Font(None, 50)  # Adjust font size as needed

        screen_width, screen_height = self.screen.get_size()
        button_diameter = 60  # Use diameter for the circle
        button_radius = button_diameter // 2
        button_center_x = (screen_width - button_diameter) // 2 + button_radius
        button_center_y = (screen_height * 0.49) + 120 + button_radius

        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    self.running = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    distance = ((mx - button_center_x) ** 2 + (my - button_center_y) ** 2) ** 0.5
                    if distance <= button_radius:
                        menu_running = False
                        self.running = False
                        return 'quit'

            self.screen.blit(background_image, (0, 0))

            # Display winning color
            text_surface = font.render(f"{winning_color.capitalize()} wins!", True, text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height * 0.48))
            self.screen.blit(text_surface, text_rect)

            # Draw hover effect
            mx, my = pygame.mouse.get_pos()
            distance = ((mx - button_center_x) ** 2 + (my - button_center_y) ** 2) ** 0.5
            button_hover = distance <= button_radius
            if button_hover:
                pygame.draw.circle(self.screen, hover_color, (button_center_x, button_center_y), button_radius)

            # Adjust text rendering to be more centered within the button
            text_surface = font.render("X", True, text_color)
            self.screen.blit(text_surface, (button_center_x - text_surface.get_width() / 2,
                                            button_center_y - text_surface.get_height() / 2))

            pygame.display.flip()

    def draw(self):
        # Draw the board
        for row in range(8):
            for col in range(8):
                color = (119, 149, 86) if (row + col) % 2 == 0 else (235, 236, 208)
                pygame.draw.rect(self.screen, color, pygame.Rect(col * 100, row * 100, 100, 100))

        # Highlight squares for the selected piece's possible moves
        if self.selected_piece:
            piece = self.board.piece_at(self.selected_piece)
            if piece:
                possible_moves = piece.possible_moves(self.board)
                for _, end_pos in possible_moves:
                    pygame.draw.rect(self.screen, (0, 255, 255),
                                     pygame.Rect(end_pos[1] * 100, end_pos[0] * 100, 100, 100), 5)

        # Draw the pieces
        if not self.is_invisible_mode:
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
        game_mode = self.display_start_menu()  # Display the start menu and get the selected game mode
        if game_mode is None:
            return

        self.is_invisible_mode = True if game_mode == 'invisible' else False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

            self.draw()
            pygame.display.flip()

            # Check for checkmate or draw
            if self.is_checkmate():
                print(f"Checkmate detected for {self.current_turn}. Game over.")
                self.display_end_menu('black' if self.current_turn == 'white' else 'white')
                self.game_over = True
            elif self.is_draw():
                print("Draw detected. Game over.")
                self.display_end_menu('draw')
                self.game_over = True

            if self.game_over:
                # Properly handle game over state
                print("Game over. Press any key to exit.")
                pygame.event.wait()  # This waits for any event, consider waiting for a specific event like a key press
                self.running = False  # Stop the game loop

            pygame.time.delay(100)

    def handle_mouse_click(self, position):
        col = position[0] // 100
        row = position[1] // 100
        clicked_pos = (row, col)

        if self.selected_piece:
            start_pos = self.selected_piece
            end_pos = clicked_pos
            if self.make_move(start_pos, end_pos):
                # Move was successful, switch turns
                self.switch_turns()
                self.selected_piece = None  # Deselect the piece after successfully moving
            else:
                # Move was not successful, decide whether to deselect or reselect based on the clicked position
                self.selected_piece = None if self.board.piece_at(clicked_pos) and self.board.piece_at(clicked_pos).color != self.current_turn else clicked_pos
        else:
            # Select a piece if it belongs to the current player
            if self.board.piece_at(clicked_pos) and self.board.piece_at(clicked_pos).color == self.current_turn:
                self.selected_piece = clicked_pos

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

        valid_moves = piece.possible_moves(self.board)
        if (start_pos, end_pos) in valid_moves:
            self.board.move_piece(start_pos, end_pos, False)
            if self.board.is_in_check(self.current_turn):
                # Undo the move if it results in check
                self.board.move_piece(end_pos, start_pos, False)
                print("Move puts you in check, try another move.")
                return False
            # Move is successful
            return True
        else:
            print("Illegal move for the piece.")
            return False

    def is_checkmate(self):
        if not self.board.is_in_check(self.current_turn):
            return False

        # Get all possible moves for the current player
        all_moves = self.board.get_all_possible_moves(self.current_turn)

        for move in all_moves:
            start_pos, end_pos = move  # Unpacking the move tuple
            piece = self.board.piece_at(start_pos)
            captured_piece = self.board.piece_at(end_pos)

            # Simulate the move
            self.board.move_piece(start_pos, end_pos, True)

            # Check if the move gets the current player out of check
            still_in_check = self.board.is_in_check(self.current_turn)

            # Undo the move
            self.board.move_piece(end_pos, start_pos, True)
            if captured_piece:
                # Restore the captured piece if there was one
                self.board.board[end_pos[0]][end_pos[1]] = captured_piece
            else:
                # Ensure the end position is cleared if it was a simple move
                self.board.board[end_pos[0]][end_pos[1]] = None

            # Restore the piece's original position
            self.board.board[start_pos[0]][start_pos[1]] = piece

            if not still_in_check:
                # Found a move that can escape check, so it's not checkmate
                return False

        # If no moves escape check, it's checkmate
        return True

    def is_draw(self):
        # Check for stalemate: no legal moves but not in check
        if not self.board.is_in_check(self.current_turn):
            all_possible_moves = self.board.get_all_possible_moves(self.current_turn)
            if not all_possible_moves:
                print("Draw due to stalemate.")
                return True

        # Check for insufficient material: only kings left, or kings with a bishop/knight
        pieces = [piece for row in self.board.board for piece in row if piece is not None]
        if len(pieces) == 2 and all(isinstance(piece, King) for piece in pieces):
            print("Draw due to insufficient material.")
            return True
        if len(pieces) <= 4:
            piece_types = [type(piece) for piece in pieces]
            if piece_types.count(King) == 2 and (piece_types.count(Bishop) == 1 or piece_types.count(Knight) == 1):
                print("Draw due to insufficient material.")
                return True
            if piece_types.count(King) == 2 and piece_types.count(Bishop) == 2:
                bishops_on_same_color = all(
                    (piece.position[0] + piece.position[1]) % 2 == 0 for piece in pieces if isinstance(piece, Bishop))
                if bishops_on_same_color or not bishops_on_same_color:
                    print("Draw due to insufficient material.")
                    return True

        # Implement other draw conditions as needed

        return False

    @staticmethod
    def main():
        game_instance = game_main()
        game_instance.play()

if __name__ == "__main__":
    game_main.main()
