#!/usr/bin/env python

import moggio.defines as defines
import moggio.cache
import moggio.state
import moggio.move
import moggio.util

moggio.cache.preprocess()

position = moggio.state.State(defines.FEN_TEST)
print position

for move in moggio.move.generate_moves(position):
    print move
