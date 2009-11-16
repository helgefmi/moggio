import moggio.util
import moggio.defines as defs

"""Includes the State class."""

class State:

    """Represents the state of a position on the chess board.

        This class has the variables:
        pieces      - Set of bitboards representing the pieces position on the board.
        turn        - Who's turn it is.
        castling    - Castling availability.
        en_passant  - En passant availability.
        occupied    - Which squares are occupied by white, black, or both.
    """

    def __init__(self, fen=None):
        """If fen is not given, the instance will represent an empty board."""
        self.reset()

        if fen:
            self.set_fen(fen)

    def reset(self):
        """Forgets everything about the current state."""
        self.pieces = (
            [0, 0, 0, 0, 0, 0], # WHITE
            [0, 0, 0, 0, 0, 0]  # BLACK
        )
        self.turn = defs.WHITE
        self.castling = 0
        self.en_passant = 0
        self.occupied = [
            0, 0, 0 # WHITE, BLACK, BOTH
        ]

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

        # Update self.occupied with the occupied squares in self.pieces.
        moggio.util.set_occupied(self.occupied, self.pieces)

        # Set active color.
        fen_color = fen_parts.pop(0)

        if fen_color.lower() == 'w':
            self.turn = defs.WHITE
        elif fen_color.lower() == 'b':
            self.turn = defs.BLACK
        else:
            raise Exception("Invalid FEN: '%s'" % fen)

        # Set castling availability.
        fen_castling = fen_parts.pop(0)
        for c in fen_castling:
            if c == 'Q':
                self.castling |= defs.A1
            elif c == 'K':
                self.castling |= defs.H1
            elif c == 'q':
                self.castling |= defs.A8
            elif c == 'k':
                self.castling |= defs.H8

        # Set en passant.
        fen_passant = fen_parts.pop(0)
        if fen_passant != '-':
            square_idx = moggio.util.chars_to_square(fen_passant)
            self.en_passant = (1L << square_idx)

        # TODO: Halfmove and Fullmove numbers from FEN.

    def __str__(self):
        """Makes a pretty string, representing a position."""
        seperator = '+---+---+---+---+---+---+---+---+\n'
        ret = seperator

        for y in xrange(7, -1, -1):
            ret += '|'

            for x in xrange(0, 8):
                idx = 1L << (y * 8 + x)

                found = None
                for color, piece in defs.COLOR_PIECES:
                    if self.pieces[color][piece] & idx:
                        found = moggio.util.piece_to_char(color, piece)
                        break

                extra = ' '
                if self.en_passant & idx:
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
