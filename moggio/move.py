import moggio.util
import moggio.defines as defs
import moggio.cache

"""Module containing functions for generating moves"""

class Move:
    
    """Contains all the information of a move on the chess board"""

    def __init__(self, from_square, to_square, capture=None):
        self.from_square = from_square
        self.to_square = to_square
        self.capture = capture
    
    def __str__(self):
        from_square = moggio.cache.bitpos_to_square_idx[self.from_square]
        to_square = moggio.cache.bitpos_to_square_idx[self.to_square]

        return "%s %s" % (moggio.util.square_to_char(from_square), \
                          moggio.util.square_to_char(to_square))

def generate_moves(state):
    """Generates all the valid moves/captures/promotions in a position"""
    for color, piece in defs.PIECES:
        bits = state.pieces[color][piece]

        while bits:
            from_square = bits & -bits
            bits &= bits - 1

            valid_moves = generate_piece_moves(state, color, piece, from_square)
            while valid_moves:
                to_square = valid_moves & -valid_moves
                valid_moves &= valid_moves - 1
                
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
        valid_moves = moggio.cache.pawn_move_one[color][from_square] \
                & ~state.occupied[defs.BOTH]

        if valid_moves:
            valid_moves = moggio.cache.pawn_move_two[color][from_square] \
                & ~state.occupied[defs.BOTH]

        # Check the attack-pattern against opponents and/or en passant availablility.
        valid_moves |= moggio.cache.pawn_attacks[color][from_square] \
            & (state.occupied[opponent] | state.en_passant)

    elif piece == defs.KNIGHT:
        valid_moves = moggio.cache.moves_from[defs.KNIGHT][from_square] \
            & ~state.occupied[color]

    elif piece == defs.KING:
        valid_moves = moggio.cache.moves_from[defs.KING][from_square] \
            & ~state.occupied[color]

        #TODO: Castling.
        # We need to first check if the path is free and that castling is available in that path.
        # Then we need to see if the king are attacked, or if any of the "stepping" squares
        # (F1 and G1 for white king side castle) are currently being attacked.

    else:
        #TODO: Remember to do valid_moves |= and not =, because of the queen.
        if piece == defs.BISHOP or piece == defs.QUEEN:
            pass

        if piece == defs.BISHOP or piece == defs.QUEEN:
            pass

    return valid_moves
