import moggio.defines as defs
import moggio.cache

"""Module containing functions for generating moves"""

class Move:
    
    """Contains all the information of a move on the chess board"""

    def __init__(self, from_square, to_square, capture=None):
        self.from_square = from_square
        self.to_square = to_square
        self.capture = capture

def generate_moves(state):
    """Generates all the valid moves/captures/promotions in a position"""
    for color, piece in defs.PIECES:
        bits = state.pieces[color][piece]

        while bits:
            from_square = bits & -bits

            for move in generate_piece_moves(state, from_square, color, piece):
                yield move

            bits &= bits - 1

def generate_piece_moves(state, from_square, color, piece):
    """Generates all the valid moves/captures of one specific piece in a position"""
    # TODO
    if piece == defs.PAWN:
        bits = moggio.cache.moves_from[piece][color][from_square]
        yield bits
