#!/usr/bin/env python

import moggio.state
import moggio.defines as defines
import moggio.cache

moggio.cache.preprocess()

position = moggio.state.State(defines.FEN_INIT)
print position

