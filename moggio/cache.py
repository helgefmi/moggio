"""This module contains cached variables that are used for efficiency in the moggio library."""

import moggio.util
import moggio.defines as defs

_entry = dict([(1L << x, 0) for x in range(64)])

# Every possible move for every piece on any given square.
moves_from = (
    None, # Dummy value used to be able to reference the correct
          # piece moves with moves_from[defs.KNIGHT] for example.
          # Pawn moves are defined below.
    _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy()
)

# Since pawn are special in that the moves are different from each color
# and also because it sometimes can move one and other times two steps,
# we seperate the pawn moves from the other pieces, which have no special
# rules.
pawn_attacks  = (_entry.copy(), _entry.copy())
pawn_move_one = (_entry.copy(), _entry.copy())
pawn_move_two = (_entry.copy(), _entry.copy())

# Contains a bit position -> square index mapping
bitpos_to_square_idx = dict([(1L << x, x) for x in xrange(64)])

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
                pawn_move_one[defs.WHITE][cache_idx] |= 1L << (idx + 8)
                if y == 1:
                    pawn_move_two[defs.WHITE][cache_idx] |= 1L << (idx + 16)

                pawn_move_one[defs.BLACK][cache_idx] |= 1L << (idx - 8)
                if y == 6:
                    pawn_move_two[defs.BLACK][cache_idx] |= 1L << (idx - 16)

                pawn_move_two[defs.WHITE][cache_idx] |= pawn_move_one[defs.WHITE][cache_idx]
                pawn_move_two[defs.BLACK][cache_idx] |= pawn_move_one[defs.BLACK][cache_idx]

                if x < 7:
                    pawn_attacks[defs.WHITE][cache_idx] |= 1L << (idx + 9)
                    pawn_attacks[defs.BLACK][cache_idx] |= 1L << (idx - 7)
                if x > 0:
                    pawn_attacks[defs.WHITE][cache_idx] |= 1L << (idx + 7)
                    pawn_attacks[defs.BLACK][cache_idx] |= 1L << (idx - 9)

            # KNIGHT
            for y2, x2 in [(y + 1, x + 2), (y - 1, x + 2), (y + 2, x + 1), (y - 2, x + 1),
                           (y + 1, x - 2), (y - 1, x - 2), (y + 2, x - 1), (y - 2, x - 1)]:
                if y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    moves_from[defs.KNIGHT][cache_idx] |= 1L << (y2 * 8 + x2)

            # BISHOP
            for ydir, xdir in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                y2 = y + ydir
                x2 = x + xdir
                while y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    moves_from[defs.BISHOP][cache_idx] |= 1L << (y2 * 8 + x2)
                    y2 = y2 + ydir
                    x2 = x2 + xdir

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

            # QUEEN
            moves_from[defs.QUEEN][cache_idx] = moves_from[defs.BISHOP][cache_idx] \
                                        | moves_from[defs.ROOK][cache_idx]
            
            # KING
            for ydir, xdir in [(1, 0), (1, 1), (0, 1), (-1, 1), \
                               (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                y2 = y + ydir
                x2 = x + xdir
                if x2 >= 0 and y2 >= 0 and x2 <= 7 and y2 <= 7:
                    moves_from[defs.KING][cache_idx] |= 1L << (y2 * 8 + x2)
