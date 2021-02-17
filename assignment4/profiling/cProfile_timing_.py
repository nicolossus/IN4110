#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cProfile
import io
import pstats

from test_slow_rectangle import random_array, snake_loop

n_experiments = 5
array = random_array(1e5)

pr = cProfile.Profile()
pr.enable()
res = pr.run(f'snake_loop(array)')
pr.disable()

s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()

with open("cProfile_report.txt", "w") as f:
    f.write(s.getvalue())

# additional comments
with open("cProfile_report.txt", "a") as f:
    str1 = "cProfile's 'snake_loop' result is similar to time.time's (see comment in timeit report). "
    str2 = "cProfile is a useful tool to identify potential bottlenecks in the calls within the function."
    strs = [str1, str2]
    for str_ in strs:
        f.write("\n" + str_)
