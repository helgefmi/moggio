import string

import moggio.defines as defs

"""A collection of helper-functions for the moggio library."""

# Used to convert numerical indices to character-representation and backwards.
_pieces_to_int = {
    'p': defs.PAWN,      'P': defs.PAWN,
    'n': defs.KNIGHT,    'N': defs.KNIGHT,
    'b': defs.BISHOP,    'B': defs.BISHOP,
    'r': defs.ROOK,      'R': defs.ROOK,
    'q': defs.QUEEN,     'Q': defs.QUEEN,
    'k': defs.KING,      'K': defs.KING
}


def char_to_piece(c):
    """Converts a piece in character-representation to its numerical piece-value."""
    return _pieces_to_int[c]

def char_to_color(c):
    """Converts a piece in character-representation to its numerical color-value."""
    if c in string.uppercase:
        return defs.WHITE
    else:
        return defs.BLACK


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

    if color == defs.WHITE:
        ret = ret.upper()
    else:
        ret = ret.lower()

    return ret


def square_to_chars(square_idx):
    """Converts a numerical square value to its chess representation (0 == a1, 1 = b1, etc)"""
    y, x = square_idx / 8 + 1, square_idx % 8
    return "%s%d" % (chr(ord('a') + x), y)


def int_to_bitmap(n):
    """Converts a 64bit integer to a bitmap string-representation."""

    ret = ''
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
    occupied[defs.WHITE] = occupied[defs.BLACK] = occupied[defs.BOTH] = 0

    for color, piece in defs.PIECES:
        occupied[color] |= pieces[color][piece]
        occupied[defs.BOTH] |= pieces[color][piece]
