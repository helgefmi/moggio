import moggio.util as util
import moggio.defines as defs
import moggio.cache as cache

"""Module containing functions for generating moves"""

class Move:
    
    """Contains all the information of a move on the chess board"""

    def __init__(self, from_square, to_square, capture=None):
        self.from_square = from_square
        self.to_square = to_square
        self.capture = capture
    
    def __str__(self):
        from_square = cache.bitpos_to_square_idx[self.from_square]
        to_square = cache.bitpos_to_square_idx[self.to_square]

        return "%s %s" % (util.square_to_chars(from_square), \
                          util.square_to_chars(to_square))

def generate_moves(state):
    """Generates all the valid moves/captures/promotions in a position"""
    color = state.turn
    for piece in xrange(defs.KING + 1):
        bits = state.pieces[color][piece]

        while bits:
            from_square = bits & -bits
            bits &= bits - 1L

            valid_moves = generate_piece_moves(state, color, piece, from_square)
            while valid_moves:
                to_square = valid_moves & -valid_moves
                valid_moves &= valid_moves - 1L
                
                move = Move(from_square, to_square)
                yield move

            moves = 0

def generate_piece_moves(state, color, piece, from_square):
    """Generates all the valid moves/captures of one specific piece in a position"""
    valid_moves = 0
    opponent = 1 - color

    if piece == defs.PAWN:
        # First, we check if a one-step move is available, and if so,
        # we set valid_moves to two steps forwards (since we know
        # that the first step wasn't blocked by a piece).
        valid_moves = cache.moves_pawn_one[color][from_square] \
                & ~state.occupied[defs.BOTH]

        if valid_moves:
            valid_moves = cache.moves_pawn_two[color][from_square] \
                & ~state.occupied[defs.BOTH]

        valid_moves |= cache.attacks_pawn[color][from_square] \
            & state.en_passant

        # Check the attack-pattern against opponents and/or en passant availablility.
        valid_moves |= cache.attacks_pawn[color][from_square] \
            & state.occupied[opponent]

    elif piece == defs.KNIGHT:
        valid_moves = cache.moves_knight[from_square] \
            & ~state.occupied[color]

    elif piece == defs.KING:
        valid_moves = cache.moves_king[from_square] \
            & ~state.occupied[color]

        # We need to first check if the path is free and that castling is available in that path.
        # Then we need to see if the king or any of the "stepping" squares (F1 and G1 for white king side castle)
        # are being attacked.

        left_castle = cache.castling_availability[color][0][from_square]
        if left_castle & state.castling:
            steps = cache.castling_steps[color][0]
            if (not steps & state.occupied[defs.BOTH]) \
                and not is_attacked(state, steps | from_square, opponent):
                valid_moves |= left_castle << 2

        right_castle = cache.castling_availability[color][1][from_square]
        if right_castle & state.castling:
            steps = cache.castling_steps[color][1]
            if (not steps & state.occupied[defs.BOTH]) \
                and not is_attacked(state, steps | from_square, opponent):
                valid_moves |= right_castle >> 1
    else:
        # TODO: Needs more rotated bitboards!
        if piece == defs.BISHOP or piece == defs.QUEEN:
            nw_moves = cache.directions[defs.NW][from_square] & state.occupied[defs.BOTH]
            nw_moves = (nw_moves << 7) | (nw_moves << 14) \
                        | (nw_moves << 21) | (nw_moves << 28) \
                        | (nw_moves << 35) | (nw_moves << 42)
            nw_moves &= cache.directions[defs.NW][from_square]
            nw_moves ^= cache.directions[defs.NW][from_square]

            ne_moves = cache.directions[defs.NE][from_square] & state.occupied[defs.BOTH]
            ne_moves = (ne_moves << 9) | (ne_moves << 18) \
                        | (ne_moves << 27) | (ne_moves << 36) \
                        | (ne_moves << 45) | (ne_moves << 54)
            ne_moves &= cache.directions[defs.NE][from_square]
            ne_moves ^= cache.directions[defs.NE][from_square]

            se_moves = cache.directions[defs.SE][from_square] & state.occupied[defs.BOTH]
            se_moves = (se_moves >> 7) | (se_moves >> 14) \
                        | (se_moves >> 21) | (se_moves >> 28) \
                        | (se_moves >> 35) | (se_moves >> 42)
            se_moves &= cache.directions[defs.SE][from_square]
            se_moves ^= cache.directions[defs.SE][from_square]

            sw_moves = cache.directions[defs.SW][from_square] & state.occupied[defs.BOTH]
            sw_moves = (sw_moves >> 9) | (sw_moves >> 18) \
                        | (sw_moves >> 27) | (sw_moves >> 36) \
                        | (sw_moves >> 45) | (sw_moves >> 54)
            sw_moves &= cache.directions[defs.SW][from_square]
            sw_moves ^= cache.directions[defs.SW][from_square]

            valid_moves |= (nw_moves | ne_moves | se_moves | sw_moves) \
                & ~state.occupied[color]

        if piece == defs.ROOK or piece == defs.QUEEN:
            right_moves = cache.directions[defs.EAST][from_square] & state.occupied[defs.BOTH]
            right_moves = (right_moves << 1) | (right_moves << 2) \
                        | (right_moves << 3) | (right_moves << 4) \
                        | (right_moves << 5) | (right_moves << 6)
            right_moves &= cache.directions[defs.EAST][from_square]
            right_moves ^= cache.directions[defs.EAST][from_square]

            left_moves = cache.directions[defs.WEST][from_square] & state.occupied[defs.BOTH]
            left_moves = (left_moves >> 1) | (left_moves >> 2) \
                        | (left_moves >> 3) | (left_moves >> 4) \
                        | (left_moves >> 5) | (left_moves >> 6)
            left_moves &= cache.directions[defs.WEST][from_square]
            left_moves ^= cache.directions[defs.WEST][from_square]

            up_moves = cache.directions[defs.NORTH][from_square] & state.occupied[defs.BOTH]
            up_moves = (up_moves << 8) | (up_moves << 16) \
                        | (up_moves << 24) | (up_moves << 32) \
                        | (up_moves << 40) | (up_moves << 48)
            up_moves &= cache.directions[defs.NORTH][from_square]
            up_moves ^= cache.directions[defs.NORTH][from_square]

            down_moves = cache.directions[defs.SOUTH][from_square] & state.occupied[defs.BOTH]
            down_moves = (down_moves >> 8) | (down_moves >> 16) \
                        | (down_moves >> 24) | (down_moves >> 32) \
                        | (down_moves >> 40) | (down_moves >> 48)
            down_moves &= cache.directions[defs.SOUTH][from_square]
            down_moves ^= cache.directions[defs.SOUTH][from_square]

            valid_moves |= (right_moves | left_moves | up_moves | down_moves) \
                & ~state.occupied[color]

    return valid_moves


def is_attacked(state, squares, attacker):
    """Checks if a set of squares are currently attacked by a colors pieces"""
    defender = 1 - attacker

    while squares:
        square = squares & -squares
        squares &= squares - 1L

        # Checking whether a pawn, knight or a king is attacking a square by using
        # bitwise or on the squares they can possibly attack from.
        if state.pieces[attacker][defs.PAWN] & cache.attacked_by_pawn[attacker][square]:
            return True

        if state.pieces[attacker][defs.KNIGHT] & cache.moves_knight[square]:
            return True

        if state.pieces[attacker][defs.KING] & cache.moves_king[square]:
            return True

        # TODO:
        # This can be much faster if we check every direction (4 for bishop, 4 for rooks),
        # and see if the direction from that square hits bishop_and_queen / rook_and_queen.
        # We need to alternate between using the highest and the lowest bit to bitwise and
        # both rook and bishop moves.

        # Pretend to generate moves from the defenders POV, and see if the valid moves fits witH
        # a black bishop, rook or queen on the board.
        bishop_and_queen = state.pieces[attacker][defs.BISHOP] | state.pieces[attacker][defs.QUEEN]
        if bishop_and_queen & generate_piece_moves(state, defender, defs.BISHOP, square):
            return True

        rook_and_queen = state.pieces[attacker][defs.ROOK] | state.pieces[attacker][defs.QUEEN]
        if rook_and_queen & generate_piece_moves(state, defender, defs.ROOK, square):
            return True

    return False
