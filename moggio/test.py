"""Class used for testing the engine; perft and divide are found here"""

import moggio.move
import moggio.defines as defs

def perft(state, depth, start=True):
    if depth == 0:
        res = moggio.move.is_attacked(
            state,
            state.pieces[1 - state.turn][defs.KING],
            state.turn
        )

        return not res

    moves = moggio.move.generate_moves(state)

    if len(moves) == 0:
        return 0

    nodes = 0
    for move in moves:
        duplicate = state.copy()
        duplicate.make_move(move)

        res = perft(duplicate, depth - 1, False);

        if start and res:
            print "%s: %d" % (move, res)

        nodes += res
        #state.unmake_move(move)

    return nodes
