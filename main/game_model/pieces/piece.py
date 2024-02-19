# game_model/pieces/piece.py

class Piece:
    def __init__(self, color, name, position):
        self.color = color
        self.name = name
        self.position = position  # Position is a tuple (row, col)

    def possible_moves(self, board):
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        color_char = 'w' if self.color == 'white' else 'b'
        return f"{color_char}{self.name}"

