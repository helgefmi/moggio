import moggio.util
from moggio.defines import *

"""Includes the State class"""

class State:

    """Represents the state of a position on the chess board

        This class has the variables:
        pieces      - set of bitboards
        turn        - Who's turn it is
        castling    - Castling availability
        en_passant  - En passant availability
    """

    def __init__(self, fen=None):
        """If fen is not given, the instance will represent an empty board."""
        self.reset()

        if fen:
            self.set_fen(fen)

    def reset(self):
        """Forgets everything about the current state."""
        self.pieces = (
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        )
        self.turn = WHITE
        self.castling = 0
        self.en_passant = None

    def set_fen(self, fen):
        """Sets the board according to Forsyth-Edwards Notation.
        
           See http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation for more information.
        """
        self.reset()

        fen_parts = fen.split()
        numbers = map(str, range(1, 10))

        # Set up the position
        fen_position = fen_parts.pop(0)
        piece_idx = 8 * 7 # Starting on the A8.

        for c in fen_position:
            if c == '/':
                piece_idx -= 2 * 8

            elif c in numbers:
                piece_idx += int(c)

            else:
                try:
                    piece = moggio.util.char_to_piece(c)
                    color = moggio.util.char_to_color(c)
                    self.pieces[color][piece] |= (1L << piece_idx)
                except KeyError:
                    raise Exception("Invalid FEN: '%s'" % fen)
                else:
                    piece_idx += 1

        # Set active color
        fen_color = fen_parts.pop(0)

        if fen_color.lower() == 'w':
            self.turn = WHITE
        elif fen_color.lower() == 'b':
            self.turn = BLACK
        else:
            raise Exception("Invalid FEN: '%s'" % fen)

        # Set castling availability
        fen_castling = fen_parts.pop(0)
        for c in fen_castling:
            if c == 'Q':
                self.castling |= 1L << 0
            elif c == 'K':
                self.castling |= 1L << 7
            elif c == 'q':
                self.castling |= 1L << (7 * 8)
            elif c == 'k':
                self.castling |= 1L << (7 * 8 + 7)

        # Set en passant
        fen_passant = fen_parts.pop(0)
        if fen_passant != '-':
            square_idx = moggio.util.chars_to_square(fen_passant)
            self.en_passant = (1L << square_idx)

        # TODO: Halfmove and Fullmove numbers from FEN

    def __str__(self):
        """Makes a pretty string, representing a position"""
        seperator = '+---+---+---+---+---+---+---+---+\n'
        ret = seperator

        for y in xrange(7, -1, -1):
            ret += '|'

            for x in xrange(0, 8):
                idx = 1L << (y * 8 + x)

                found = None
                for color, piece in PIECES:
                    if self.pieces[color][piece] & idx:
                        found = moggio.util.piece_to_char(color, piece)
                        break

                extra = ' '
                if self.en_passant and self.en_passant & idx:
                    extra = '*'
                if self.castling and self.castling & idx:
                    extra = '*'

                if found:
                    ret += ' ' + moggio.util.piece_to_char(color, piece) + extra + '|'
                else:
                    squareColor = '  '
                    if (y ^ x) & 1 == 0:
                        squareColor = ' .'
                    ret += squareColor + extra + '|'

            ret += "\n" + seperator

        ret += 'Turn: %s' % ('White', 'Black')[self.turn]
        ret += "\n"

        return ret

def fen_to_state(fen):
    b = Board()
    return b
