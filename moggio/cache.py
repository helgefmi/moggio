"""This module contains cached variables that are used for efficiency in the moggio library."""

import moggio.util
import moggio.defines as defs

_entry = dict([(1L << x, 0) for x in range(64)])

# Since pawn are special in that the moves are different from each color
# and also because it sometimes can move one and other times two steps,
# we use three variables to cache the moves.
attacks_pawn  = (_entry.copy(), _entry.copy())
moves_pawn_one = (_entry.copy(), _entry.copy())
moves_pawn_two = (_entry.copy(), _entry.copy())

# Kinda the inverse of attacks_pawn; the bits says where a pawn must be positioned
# to attack a certain square
attacked_by_pawn = (_entry.copy(), _entry.copy())

# Knight and king moves are very easy to calculate, and only needs one dictionary each.
moves_knight = _entry.copy()
moves_king = _entry.copy()

# Bishop, Rooks and Queen moves can be combined from rays going in every direction.
directions = (
    _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy(),
    _entry.copy(), _entry.copy(), _entry.copy(), _entry.copy()
)

# Contains a bit position -> square index mapping
# Should probably not be used in inner loops :-)
bitpos_to_square_idx = dict([(1L << x, x) for x in xrange(64)])

# Used to efficiently find out if castling is available
castling_availability = ((_entry.copy(), _entry.copy()),
                         (_entry.copy(), _entry.copy()))

# Used to efficiently find out if there are any pieces blocking a castle
castling_steps = ([0, 0], [0, 0])

# Used to efficiently find out if a pawn can promote (basically set to
# rank #8 for white and rank #1 for black)
promotion_rank = [0, 0]

def preprocess():
    """Sets up moves_from and attacks_from.
    
       Should only be called once.
    """
    castling_availability[defs.WHITE][0][defs.E1] = defs.A1
    castling_availability[defs.WHITE][1][defs.E1] = defs.H1
    castling_availability[defs.BLACK][0][defs.E1] = defs.A8
    castling_availability[defs.BLACK][1][defs.E1] = defs.H8

    castling_steps[defs.WHITE][0] = defs.C1 | defs.D1
    castling_steps[defs.WHITE][1] = defs.F1 | defs.G1

    castling_steps[defs.BLACK][0] = defs.C8 | defs.D8
    castling_steps[defs.BLACK][1] = defs.F8 | defs.G8

    promotion_rank[defs.WHITE] = defs.A8 | defs.B8 | defs.C8 | defs.D8 \
                                  | defs.E8 | defs.F8 | defs.G8 | defs.H8
    promotion_rank[defs.BLACK] = defs.A1 | defs.B1 | defs.C1 | defs.D1 \
                                  | defs.E1 | defs.F1 | defs.G1 | defs.H1

    for y in xrange(0, 8):
        for x in xrange(0, 8):
            idx = y * 8 + x
            cache_idx = 1L << idx

            # PAWN
            if y > 0 and y < 7:
                moves_pawn_one[defs.WHITE][cache_idx] |= 1L << (idx + 8)
                if y == 1:
                    moves_pawn_two[defs.WHITE][cache_idx] |= 1L << (idx + 16)

                moves_pawn_one[defs.BLACK][cache_idx] |= 1L << (idx - 8)
                if y == 6:
                    moves_pawn_two[defs.BLACK][cache_idx] |= 1L << (idx - 16)

                moves_pawn_two[defs.WHITE][cache_idx] |= moves_pawn_one[defs.WHITE][cache_idx]
                moves_pawn_two[defs.BLACK][cache_idx] |= moves_pawn_one[defs.BLACK][cache_idx]

                if x < 7:
                    attacks_pawn[defs.WHITE][cache_idx] |= 1L << (idx + 9)
                    attacks_pawn[defs.BLACK][cache_idx] |= 1L << (idx - 7)
                if x > 0:
                    attacks_pawn[defs.WHITE][cache_idx] |= 1L << (idx + 7)
                    attacks_pawn[defs.BLACK][cache_idx] |= 1L << (idx - 9)

            if y > 1:
                if x < 7:
                    attacked_by_pawn[defs.WHITE][cache_idx] |= 1L << (idx - 7)
                if x > 0:
                    attacked_by_pawn[defs.WHITE][cache_idx] |= 1L << (idx - 9)
            if y < 6:
                if x < 7:
                    attacked_by_pawn[defs.BLACK][cache_idx] |= 1L << (idx + 9)
                if x > 0:
                    attacked_by_pawn[defs.BLACK][cache_idx] |= 1L << (idx + 7)

            # KNIGHT
            for y2, x2 in [(y + 1, x + 2), (y - 1, x + 2), (y + 2, x + 1), (y - 2, x + 1),
                           (y + 1, x - 2), (y - 1, x - 2), (y + 2, x - 1), (y - 2, x - 1)]:
                if y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    moves_knight[cache_idx] |= 1L << (y2 * 8 + x2)

            # BISHOP & QUEEN
            for ydir, xdir, dir in [(1, 1, defs.NE), (1, -1, defs.NW), \
                                    (-1, 1, defs.SE), (-1, -1, defs.SW)]:
                y2 = y + ydir
                x2 = x + xdir
                while y2 >= 0 and x2 >= 0 and y2 <= 7 and x2 <= 7:
                    directions[dir][cache_idx] |= 1L << (y2 * 8 + x2)
                    y2 = y2 + ydir
                    x2 = x2 + xdir

            # ROOK & QUEEN
            for ydir, xdir, dir in [(1, 0, defs.NORTH), (0, 1, defs.EAST), \
                        (-1, 0, defs.SOUTH), (0, -1, defs.WEST)]:
                x2 = x + xdir
                y2 = y + ydir
                while x2 >= 0 and y2 >= 0 and x2 <= 7 and y2 <= 7:
                    directions[dir][cache_idx] |= 1L << (y2 * 8 + x2)
                    x2 += xdir
                    y2 += ydir

            # KING
            for ydir, xdir in [(1, 0), (1, 1), (0, 1), (-1, 1), \
                               (-1, 0), (-1, -1), (0, -1), (1, -1)]:
                y2 = y + ydir
                x2 = x + xdir
                if x2 >= 0 and y2 >= 0 and x2 <= 7 and y2 <= 7:
                    moves_king[cache_idx] |= 1L << (y2 * 8 + x2)
