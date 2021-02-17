#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import numpy as np


def timer(n_experiments, func, *args, **kwargs):
    """
    Measure run time averaged over n experiments of a function using time.time 

    Arguments
    ---------
    n_experiments : int
        Number of experiments (or runs) to average time usage over
    func : object
        Function object to profile
    *args
        Arbitrary arguments passed along to func
    **kwargs
            Arbitrary keyword arguments passed along to func

    Returns
    -------
    output : str
        Nicely formated string of profile result
    run_time_avg : float
        Averaged run time

    Raises
    ------
    ValueError : if 'method' is not one of ['python', 'numpy', 'numba', 'cython']
    """
    run_times = np.zeros(n_experiments)
    for i in range(n_experiments):
        t0 = time.time()
        value = func(*args, **kwargs)
        run_times[i] = time.time() - t0
    run_time_avg = np.mean(run_times)
    output = f"Average run time of {func.__name__!r} after {n_experiments} runs: {run_time_avg:.5f} secs\n"
    return output, run_time_avg


def timer_results(n_experiments, filename, funcs, args, order="fast"):
    """
    Write timing results of one or more functions to file.

    If multiple functions are profiled, the slowest and fastest is identified.
    The functions are also compared with respect to (w.r.t.) the function
    specified by the value of the 'order' keyword.

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
    order : str, optional, default 'fast'
        Which order to compare profiled functions. The 'order' keyword must be
        'fast', 'slow' or one of the profiled function's name. 'fast' is w.r.t.
        the fastest function, 'slow' w.r.t. the slowest function and function
        name w.r.t. the specified function

    Raises
    ------
    ValueError : if 'order' is not 'fast', 'slow' or one of the profiled
                 function's name
    """
    outputs = []
    func_times = {}
    func_names = [func.__name__ for func in funcs]

    # Iterate over function(s) to time profile and store results
    for func, arg in zip(funcs, args):
        outputs.append(f"Timing: {func.__name__!r}")
        output, run_time = timer(n_experiments, func, arg)
        func_times[f"{func.__name__}"] = run_time
        outputs.append(output)

    # If timing more than one function
    if len(funcs) > 1:
        fastest_func = min(func_times, key=func_times.get)
        slowest_func = max(func_times, key=func_times.get)
        outputs.append(f"{fastest_func!r} is the fastest")
        outputs.append(f"{slowest_func!r} is the slowest")

        # If time comparisons should be w.r.t. the fastest function
        if order == "fast":
            for key, value in func_times.items():
                if key != fastest_func:
                    outputs.append(
                        f"{fastest_func!r} is {value/func_times[fastest_func]:.2f} times faster than {key!r}")

        # If time comparisons should be w.r.t. the slowest function
        elif order == "slow":
            for key, value in func_times.items():
                if key != slowest_func:
                    outputs.append(
                        f"{key!r} is {func_times[slowest_func]/value:.2f} times faster than {slowest_func!r}")

        # If time comparisons should be w.r.t. specified function
        elif order in func_names:
            for key, value in func_times.items():
                if key != order:
                    if func_times[order] < func_times[key]:
                        speed = "faster"
                    if func_times[order] > func_times[key]:
                        speed = "slower"
                    outputs.append(
                        f"{order!r} is {value/func_times[order]:.2f} times {speed} than {key!r}")

        # Invalid keyword
        else:
            raise ValueError(
                "'order' keyword must be 'fast', 'slow' or one of the profiled function's name")

        # Newline for nicer formatting
        outputs.append("\nTiming performed using: 'time.time'")

    # If only one function is profiled
    else:
        outputs.append("Timing performed using: 'time.time'")

    # Write results to file
    with open(filename, "w") as f:
        f.write("\n".join(outputs))


if __name__ == "__main__":
    from test_slow_rectangle import loop, random_array, snake_loop
    n_experiments = 5
    array = random_array(1e5)

    funcs = [random_array, loop, snake_loop]
    args = [1e5, array, array]

    timer_results(n_experiments, "manual_report.txt",
                  funcs, args, order="slow")
