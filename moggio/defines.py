"""Some convenient variables to make the rest of the code clearer."""

FEN_INIT = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

WHITE = 0
BLACK = 1
BOTH = 2

PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5

PIECES = (
    (WHITE, PAWN),   (BLACK, PAWN),
    (WHITE, KNIGHT), (BLACK, KNIGHT),
    (WHITE, BISHOP), (BLACK, BISHOP),
    (WHITE, ROOK),   (BLACK, ROOK),
    (WHITE, QUEEN),  (BLACK, QUEEN),
    (WHITE, KING),   (BLACK, KING)
)
