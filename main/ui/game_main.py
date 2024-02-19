# ui/game_main.py
import pygame
import os

from main.game_model.Board import Board

# Constants for the board size
BOARD_SIZE = 600  # Size of the board in pixels
SQUARE_SIZE = BOARD_SIZE // 8  # Size of a square in pixels

# RGB color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)  # For highlighting squares


def load_images():
    """
    Loads images of chess pieces into a dictionary.
    """
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    images = {}
    for piece in pieces:
        filename = f"{piece[0].lower()}{piece[1]}.png"  # Construct the filename based on the piece names
        images[piece] = pygame.transform.scale(
            pygame.image.load(os.path.join('images', filename)),
            (SQUARE_SIZE, SQUARE_SIZE)
        )
    return images


def draw_board(screen):
    """
    Draws squares on the chessboard.
    """
    colors = [WHITE, BLACK]
    for row in range(8):
        for col in range(8):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board, images):
    """
    Draws pieces on the chessboard based on the current state of the board.board.
    """
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece is not None:
                piece_image = images[str(piece)]
                screen.blit(piece_image, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption('Chess Game')
    board = Board()
    images = load_images()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        draw_pieces(screen, board, images)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
