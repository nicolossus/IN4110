#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit

import numpy as np


def write_results(n_experiments, filename, funcs, args):
    """
    Write timing results of one or more functions to file and identify the
    slowest part.

    Arguments
    ---------
    n_experiments : int
        Number of experiments (or runs) to average time usage over
    filename : str
        Number of experiments (or runs) to average time usage over
    funcs : object
        Function object(s) to profile
    args
        Arbitrary arguments passed along to funcs in call to the timer function
    """
    outputs = []
    slowest_time = 0.0
    for func, arg in zip(funcs, args):
        reps = timeit.repeat(stmt=f"{func.__name__}({arg})", setup=f"from __main__ import {func.__name__}",
                             repeat=n_experiments, number=1)
        run_time_avg = np.mean(reps)
        output = f"Finished {func.__name__!r} in {run_time_avg:.4f} secs (averaged over {n_experiments} runs)"
        if run_time_avg > slowest_time:
            slowest_time = run_time_avg
            slowest_func = f"{func.__name__!r} is slowest\n"
        outputs.append(output)
    outputs.append(slowest_func)

    with open(filename, "w") as f:
        f.write("\n".join(outputs))


if __name__ == "__main__":
    import sys

    from test_slow_rectangle import loop, random_array, snake_loop

    n_experiments = 5
    array = random_array(1e5)
    array = np.array2string(array, separator=',', threshold=np.sys.maxsize)

    funcs = [random_array, loop, snake_loop]
    args = [1e5, array, array]

    write_results(n_experiments, "timeit_report.txt", funcs, args)

    # additional comments
    with open("timeit_report.txt", "a") as f:
        str1 = "Compared to time.time, 'random_array' and 'loop' are not quite identical but of the same order."
        str2 = "'snake_loop' however is 4-5 times faster according to timeit. This may caused by several factors"
        str3 = "and averaging over just 5 experiments are not enough to claim this is the general case."
        strs = [str1, str2, str3]
        for str_ in strs:
            f.write("\n" + str_)
