"""Some convenient variables to make the rest of the code clearer."""

FEN_INIT = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
FEN_TEST = '8/8/8/8/8/5r2/p6r/R3K2R w KQkq - 0 1'

WHITE = 0
BLACK = 1
BOTH = 2

PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
NW = 4
NE = 5
SE = 6
SW = 7

PIECES = (
    (WHITE, PAWN),   (BLACK, PAWN),
    (WHITE, KNIGHT), (BLACK, KNIGHT),
    (WHITE, BISHOP), (BLACK, BISHOP),
    (WHITE, ROOK),   (BLACK, ROOK),
    (WHITE, QUEEN),  (BLACK, QUEEN),
    (WHITE, KING),   (BLACK, KING)
)

_count = 0
for i in range(1,9):
    for j in 'abcdefgh':
        name = '%s%s' % (j,i)
        exec(name + "=" + str(1L << _count)) # a1 = 1<<7, h1 = 1
        name = name.upper()
        exec(name + "=" + str(1L << _count)) # A1 = 1<<7, H1 = 1
        _count += 1
del _count
