import moggio.util as util
import moggio.defines as defs
import moggio.cache as cache

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

    def copy(self):
        """Makes an independent copy of a state instance"""
        s = State()

        s.pieces = (
            self.pieces[0][:],
            self.pieces[1][:]
        )
        s.turn = self.turn
        s.castling = self.castling
        s.en_passant = self.en_passant
        s.occupied = self.occupied[:]

        return s

    def make_move(self, move):
        #TODO:
        # We're forgetting to set/clear en_passant!
        opponent = 1 - self.turn

        # Remove the piece that moved from the board.
        self.pieces[self.turn][move.from_piece] ^= move.from_square
        self.occupied[self.turn] ^= move.from_square

        # If it is a capture, we need to remove the opponent piece as well.
        if move.capture != None:
            # Remember to clear castling availability if we capture a rook.
            if self.castling & move.to_square:
                self.castling &= ~move.to_square

            to_remove_square = move.to_square
            if move.from_piece == defs.PAWN and move.to_square & self.en_passant:
                # The piece captured with en passant; we need to clear the board of the captured piece.
                # We simply use the pawn move square of the opponent to find out which square to clear.
                to_remove_square = cache.moves_pawn_one[opponent][move.to_square]

            # Remove the captured piece off the board.
            self.pieces[opponent][move.capture] ^= to_remove_square
            self.occupied[opponent] ^= to_remove_square

        # Update the board with the new position of the piece.
        if move.promotion:
            self.pieces[self.turn][move.promotion] ^= move.to_square
        else:
            self.pieces[self.turn][move.from_piece] ^= move.to_square

        # Update "occupied" with the same piece as above.
        self.occupied[self.turn] ^= move.to_square
        
        if move.from_piece == defs.KING:
            #TODO: This can be made more efficient by caching more stuff..
            # We could first see if the move was >1 step (one bitwise and and one lookup),
            # then we could have a cache element where cached[to_square] gives the place where
            # the rook should be positioned (one bitwise xor and one lookup).
            left_castle = cache.castling_availability[self.turn][0][move.from_square]
            if (left_castle << 2) & move.to_square:
                self.pieces[self.turn][defs.ROOK] ^= left_castle | left_castle << 3
                self.occupied[self.turn] ^= left_castle | left_castle << 3

            right_castle = cache.castling_availability[self.turn][1][move.from_square]
            if (right_castle >> 1) & move.to_square:
                self.pieces[self.turn][defs.ROOK] ^= right_castle | right_castle >> 2
                self.occupied[self.turn] ^= right_castle | right_castle >> 2

            # Clear the appropriate castling availability.
            self.castling &= ~cache.castling_by_color[self.turn]

        elif move.from_piece == defs.ROOK:
            # Clear the appropriate castling availability.
            self.castling &= ~move.from_square

        self.turn ^= 1
        self.occupied[defs.BOTH] = \
            self.occupied[defs.WHITE] | self.occupied[defs.BLACK]

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
                    piece = util.char_to_piece(c)
                    color = util.char_to_color(c)
                    self.pieces[color][piece] |= (1L << piece_idx)
                except KeyError:
                    raise Exception("Invalid FEN: '%s'" % fen)
                else:
                    piece_idx += 1

        # Update self.occupied with the occupied squares in self.pieces.
        self.occupied[defs.WHITE] = self.occupied[defs.BLACK] = self.occupied[defs.BOTH] = 0
        for color, piece in defs.COLOR_PIECES:
            self.occupied[color] |= self.pieces[color][piece]
            self.occupied[defs.BOTH] |= self.pieces[color][piece]

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
            square_idx = util.chars_to_square(fen_passant)
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
                        found = util.piece_to_char(color, piece)
                        break

                extra = ' '
                if self.en_passant & idx:
                    extra = '*'
                if self.castling and self.castling & idx:
                    extra = '*'

                if found:
                    ret += ' ' + util.piece_to_char(color, piece) + extra + '|'
                else:
                    squareColor = '  '
                    if (y ^ x) & 1 == 0:
                        squareColor = ' .'
                    ret += squareColor + extra + '|'

            ret += "\n" + seperator

        ret += 'Turn: %s' % ('White', 'Black')[self.turn]
        ret += "\n"

        return ret
