"""Class used for testing the engine; perft and divide are found here"""

import moggio.move
import moggio.defines as defs
import moggio.state
import sys
import time

def perft(state, depth, verbose=True):
    """
        Given a position, it will recursivly apply every possible
        move for a given depth and count the leaf nodes.
    """
    if depth == 0:
        res = moggio.move.is_attacked(
            state,
            state.pieces[1 - state.turn][defs.KING],
            state.turn
        )

        return not res

    moves = moggio.move.generate_moves(state)

    if not moves: # Also checks for invalid positions (if generate_moves finds a king capture, it returns None)
        return 0

    nodes = 0
    for move in moves:
        duplicate = state.copy()
        duplicate.make_move(move)

        res = perft(duplicate, depth - 1, False);

        if verbose and res:
            print "%s: %d" % (move, res)

        nodes += res
        #state.unmake_move(move)

    return nodes

def divide(state, depth):
    return perft(state, depth, True)

def perftsuite(max_depth=2):
    """Runs 126 startion position through perft() and checks if the nodecount is correct

       This tests the move generation and make/unmake moves of moggio, and should always
       have 0/126 failed.
    """
    handle = open('perftsuite.esp', 'r')
    lineno = 0
    errors = 0
    total_nodes = 0

    start_time = time.time()
    for line in handle.readlines():
        lineno += 1
        line = line.strip()

        if not line:
            continue

        fen, answers = line.split(';', 1)
        depth_answers = map(int, answers.split(';'))

        position = moggio.state.State(fen)

        sys.stdout.write('%d' % lineno)
        sys.stdout.flush()

        for depth in xrange(1, max_depth + 1):
            result = perft(position.copy(), depth, False)
            total_nodes += result

            sys.stdout.write('\t%d=%d' % (depth, result))
            sys.stdout.flush()

            correct_result = depth_answers[depth - 1]

            if result != correct_result:
                errors += 1
                sys.stdout.write("FAIL!  diff=%d depth=%d me=%d correct=%d fen=%s" % (abs(result - correct_result), depth, result, correct_result, fen));
                break

        time_spent = time.time() - start_time
        sys.stdout.write(' nps=%d\n' % (total_nodes / time_spent))

    handle.close()
    total_time = time.time() - start_time

    print "\nFailed tests: %d/%d" % (errors, lineno)
    print "%d nodes in %.2f seconds with nps=%d" % (total_nodes, total_time, total_nodes / total_time)
