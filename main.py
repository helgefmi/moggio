#!/usr/bin/env python

import moggio.defines as defines
import moggio.cache
import moggio.state
import moggio.move

moggio.cache.preprocess()

position = moggio.state.State(defines.FEN_INIT)
print position

for move in moggio.move.generate_moves(position):
    print move
