"""This module contains cached variables that are used for efficiency in the moggio library."""

import moggio.util
import moggio.defines as defs

_entry = dict([(1L << x, 0) for x in range(64)])

# Every possible move for every piece on any given square.
moves_from = (
    (_entry.copy(), _entry.copy()), # Pawns move differently depending on which color it is.
    _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy()
)

# As moves_from, but with possible attacks instead.
attacks_from = (
    (_entry.copy(), _entry.copy()), # Pawns move differently depending on which color it is.
    _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy()
)

def preprocess():
    """Sets up moves_from and attacks_from.
    
       Should only be called once.
    """
    for y in xrange(0, 8):
        for x in xrange(0, 8):
            idx = y * 8 + x
            cache_idx = 1L << idx

            # PAWN
            if y > 0 and y < 7:
                moves_from[defs.PAWN][defs.WHITE][cache_idx] |= 1L << (idx + 8)
                if y == 1:
                    moves_from[defs.PAWN][defs.WHITE][cache_idx] |= 1L << (idx + 16)

                moves_from[defs.PAWN][defs.BLACK][cache_idx] |= 1L << (idx - 8)
                if y == 6:
                    moves_from[defs.PAWN][defs.BLACK][cache_idx] |= 1L << (idx - 16)

                if x < 7:
                    attacks_from[defs.PAWN][defs.WHITE][cache_idx] |= 1L << (idx + 9)
                    attacks_from[defs.PAWN][defs.BLACK][cache_idx] |= 1L << (idx - 7)
                if x > 0:
                    attacks_from[defs.PAWN][defs.WHITE][cache_idx] |= 1L << (idx + 7)
                    attacks_from[defs.PAWN][defs.BLACK][cache_idx] |= 1L << (idx - 9)

            # KNIGHT
            for y2, x2 in [(y + 1, x + 2), (y - 1, x + 2), (y + 2, x + 1), (y - 2, x + 1),
                           (y + 1, x - 2), (y - 1, x - 2), (y + 2, x - 1), (y - 2, x - 1)]:
                if y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    moves_from[defs.KNIGHT][cache_idx] |= 1L << (y2 * 8 + x2)
            attacks_from[defs.KNIGHT][cache_idx] = moves_from[defs.KNIGHT][cache_idx]

            # BISHOP
            for ydir, xdir in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                y2 = y + ydir
                x2 = x + xdir
                while y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    moves_from[defs.BISHOP][cache_idx] |= 1L << (y2 * 8 + x2)
                    y2 = y2 + ydir
                    x2 = x2 + xdir
            attacks_from[defs.BISHOP][cache_idx] = moves_from[defs.BISHOP][cache_idx]

            # ROOK
            for dir in [1, -1]:
                x2 = x + dir
                y2 = y + dir
                while x2 >= 0 and x2 <= 7:
                    moves_from[defs.ROOK][cache_idx] |= 1L << (y * 8 + x2)
                    x2 += dir
                while y2 >= 0 and y2 <= 7:
                    moves_from[defs.ROOK][cache_idx] |= 1L << (y2 * 8 + x)
                    y2 += dir
            attacks_from[defs.ROOK][cache_idx] = moves_from[defs.ROOK][cache_idx]

            # QUEEN
            moves_from[defs.QUEEN][cache_idx] = moves_from[defs.BISHOP][cache_idx] \
                                        | moves_from[defs.ROOK][cache_idx]
            attacks_from[defs.QUEEN][cache_idx] = moves_from[defs.QUEEN][cache_idx]
            
            # KING
            for ydir, xdir in [(1, 0), (1, 1), (0, 1), (-1, 1), \
                               (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                y2 = y + ydir
                x2 = x + xdir
                if x2 >= 0 and y2 >= 0 and x2 <= 7 and y2 <= 7:
                    moves_from[defs.KING][cache_idx] |= 1L << (y2 * 8 + x2)
            attacks_from[defs.KING][cache_idx] = moves_from[defs.KING][cache_idx]
