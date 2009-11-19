#!/usr/bin/env python

try:
    import psyco
    psyco.full()
    print "Psyco loaded!"
except ImportError:
    print "Psyco not installed."
    pass

import moggio.defines as defs
import moggio.cache
import moggio.state
import moggio.test
import moggio.move

moggio.cache.preprocess()

moggio.test.perftsuite(3)

if False:
    position = moggio.state.State('8/8/8/8/PK6/8/1k6/8 b - a3 0 1')
    #move = moggio.move.Move(defs.A3, defs.B4, defs.KING)
    #position.make_move(move)

    print position
    print moggio.test.divide(position, 2)

if False:
    import cProfile, pstats
    prof = cProfile.Profile()
    prof.run('moggio.test.perftsuite(2)')

    stats = pstats.Stats(prof)
    stats.sort_stats("time")
    stats.print_stats(80)
