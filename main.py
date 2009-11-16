#!/usr/bin/env python

import moggio.defines as defines
import moggio.cache
import moggio.state
import moggio.move
import moggio.util
import moggio.test

moggio.cache.preprocess()

position = moggio.state.State(defines.FEN_TEST)

print moggio.test.perft(position, 4)
