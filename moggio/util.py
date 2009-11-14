import string

import moggio.defines as defines

"""A collection of helper-functions for the moggio library."""

# Used to convert numerical indices to character-representation and backwards.
_pieces_to_int = {
    'p': defines.PAWN,      'P': defines.PAWN,
    'n': defines.KNIGHT,    'N': defines.KNIGHT,
    'b': defines.BISHOP,    'B': defines.BISHOP,
    'r': defines.ROOK,      'R': defines.ROOK,
    'q': defines.QUEEN,     'Q': defines.QUEEN,
    'k': defines.KING,      'K': defines.KING
}


def char_to_piece(c):
    """Converts a piece in character-representation to its numerical piece-value."""
    return _pieces_to_int[c]

def char_to_color(c):
    """Converts a piece in character-representation to its numerical color-value."""
    if c in string.uppercase:
        return defines.WHITE
    else:
        return defines.BLACK


def chars_to_square(move):
    """Converts a character representation of a move (A2) to its index (8)."""
    x = ord(move[0].lower()) - ord('a')
    y = int(move[1]) - 1
    return y * 8 + x


def piece_to_char(color, piece):
    """Converts a color/piece pair into a single character."""
    ret = None

    for key in _pieces_to_int:
        if _pieces_to_int[key] == piece:
            ret = key
            break

    if color == defines.WHITE:
        ret = ret.upper()
    else:
        ret = ret.lower()

    return ret


def int_to_bitmap(n):
    """Converts a 64bit integer to a bitmap string-representation."""

    ret = ''
    # Iterate in the order of a chess board (A1 has index 0)
    for y in xrange(7, -1, -1):
        for x in xrange(0, 8):
            idx = y * 8 + x

            if n & (1L << idx):
                ret += '*'
            else:
                ret += '.'
        ret += '\n'

    return ret

def set_occupied(occupied, pieces):
    """Sets up 'occupied' to reflect the occupied squares in 'pieces'
    
       Both parameters are a part of the State class
    """
    occupied[defines.WHITE] = occupied[defines.BLACK] = occupied[defines.BOTH] = 0

    for color, piece in defines.PIECES:
        occupied[color] |= pieces[color][piece]
        occupied[defines.BOTH] |= pieces[color][piece]
