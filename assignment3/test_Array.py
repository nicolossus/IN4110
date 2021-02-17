#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Note: Each test function test the class methods for both 1D and 2D arrays
via pytest's parametrize functionality
"""


import numpy as np
import pytest

from Array import Array


# Test __str__
@pytest.mark.parametrize(
    "arg, expected",
    [
        [((3,), (2, 3, 4)), [2, 3, 4]],
        [((3,), (True, False, True)), [True, False, True]],
        [((2, 3), (1, 2, 3, 4, 5, 6)), [[1, 2, 3], [4, 5, 6]]],
        [((2, 3), (True, False, True, True, False, True)),
         [[True, False, True], [True, False, True]]]
    ]
)
def test__str__(arg, expected):
    """
    Check that print function returns the nice string
    """
    my_arr = Array(arg[0], *arg[1])
    assert my_arr.__str__() == str(expected)


# test __add__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [4, 5, 6]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [4.0, 5.0, 6.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [3, 5, 7]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [3.0, 4.0, 5.0, 6.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [5, 5, 5, 5]]
    ]
)
def test__add__(arg, other, expected):
    """
    Verify that adding to array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = my_arr + other_
    assert new_arr.flatten == expected


# test __radd__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [4, 5, 6]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [4.0, 5.0, 6.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [3, 5, 7]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [3.0, 4.0, 5.0, 6.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [5, 5, 5, 5]]
    ]
)
def test__radd__(arg, other, expected):
    """
    Verify that adding to array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = other_ + my_arr
    assert new_arr.flatten == expected


# test __sub__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [0, 1, 2]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [0.0, 1.0, 2.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [1, 1, 1]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [-1.0, 0.0, 1.0, 2.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [-3, -1, 1, 3]]
    ]
)
def test__sub__(arg, other, expected):
    """
    Verify that subtracting from array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = my_arr - other_
    assert new_arr.flatten == expected


# test __rsub__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [0, -1, -2]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [0.0, -1.0, -2.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [-1, -1, -1]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [1.0, 0.0, -1.0, -2.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [3, 1, -1, -3]]
    ]
)
def test__rsub__(arg, other, expected):
    """
    Verify that subtracting from array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = other_ - my_arr
    assert new_arr.flatten == expected


# test __mul__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [4, 6, 8]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [4.0, 6.0, 8.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [2, 6, 12]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [2.0, 4.0, 6.0, 8.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [4, 6, 6, 4]]
    ]
)
def test__mul__(arg, other, expected):
    """
    Verify that multiplying array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = my_arr * other_
    assert new_arr.flatten == expected


# test __rmul__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), (2), [4, 6, 8]],
        [((3,), (2.0, 3.0, 4.0)), (2.0), [4.0, 6.0, 8.0]],
        [((3,), (2, 3, 4)), (1, 2, 3), [2, 6, 12]],
        [((2, 2), (1.0, 2.0, 3.0, 4.0)), (2.0), [2.0, 4.0, 6.0, 8.0]],
        [((2, 2), (1, 2, 3, 4)), (4, 3, 2, 1), [4, 6, 6, 4]]
    ]
)
def test__rmul__(arg, other, expected):
    """
    Verify that multiplying array element-wise returns what it's supposed to
    """
    if isinstance(other, (int, float)):
        other_ = other
    else:
        other_ = Array(arg[0], *other)
    my_arr = Array(arg[0], *arg[1])
    new_arr = other_ * my_arr
    assert new_arr.flatten == expected


# test __eq__
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), ((3,), (2, 3, 4)), True],
        [((3,), (2, 3, 4)), ((3,), (1, 3, 4)), False],
        [((3,), (2, 3, 4)), ((2,), (2, 3)), False],
        [((2, 2), (1, 2, 3, 4)), ((2, 2), (1, 2, 3, 4)), True],
        [((2, 2), (1, 2, 3, 4)), ((2, 2), (0, 2, 3, 4)), False],
        [((2, 2), (1, 2, 3, 4)), ((3, 2), (1, 2, 3, 4, 5, 6)), False]
    ]
)
def test__eq__(arg, other, expected):
    """
    Verify that comparison of arrays evaluates correctly
    """
    my_arr = Array(arg[0], *arg[1])
    other_arr = Array(other[0], *other[1])
    bool = (my_arr == other_arr)
    assert bool == expected


# Test __getitem__
@pytest.mark.parametrize(
    "arg, index, expected",
    [
        [((3,), (2, 3, 4)), 0, 2],
        [((3,), (True, False, True)), 1, False],
        [((2, 2), (1, 2, 3, 4)), 0, [1, 2]]
    ]
)
def test__getitem__(arg, index, expected):
    """
    Verify if __getitem__ is implemented correctly
    """
    my_arr = Array(arg[0], *arg[1])
    assert my_arr[index] == expected


# test is_equal
@pytest.mark.parametrize(
    "arg, other, expected",
    [
        [((3,), (2, 3, 4)), ((3,), (2, 3, 4)), [True, True, True]],
        [((3,), (2, 3, 4)), ((3,), (2, 0, 4)), [True, False, True]],
        [((2, 2), (1, 2, 3, 4)), ((2, 2), (1, 2, 3, 4)), [True, True, True, True]]
    ]
)
def test_is_equal(arg, other, expected):
    """
    Verify that comparison of arrays evaluates correctly
    """
    my_arr = Array(arg[0], *arg[1])
    other_arr = Array(other[0], *other[1])
    assert my_arr.is_equal(other_arr).flatten == expected


# test mean
@pytest.mark.parametrize(
    "arg, np_arg",
    [
        [((3,), (2, 3, 4)), [2, 3, 4]],
        [((4,), (1.0, 2.0, 3.0, 4.0)), [1.0, 2.0, 3.0, 4.0]],
        [((2, 3), (1, 2, 3, 4, 5, 6)), [[1, 2, 3], [4, 5, 6]]]
    ]
)
def test_mean(arg, np_arg):
    """
    Verify that mean of array values is correct
    """
    my_arr = Array(arg[0], *arg[1])
    np_arr = np.array(np_arg)
    assert my_arr.mean() == pytest.approx(np.mean(np_arr))


# test variance
@pytest.mark.parametrize(
    "arg, np_arg",
    [
        [((3,), (2, 3, 4)), [2, 3, 4]],
        [((4,), (1.0, 2.0, 3.0, 4.0)), [1.0, 2.0, 3.0, 4.0]],
        [((2, 3), (1, 2, 3, 4, 5, 6)), [[1, 2, 3], [4, 5, 6]]]
    ]
)
def test_variance(arg, np_arg):
    """
    Verify that variance of array values is correct
    """
    my_arr = Array(arg[0], *arg[1])
    np_arr = np.array(np_arg)
    assert my_arr.variance() == pytest.approx(np.var(np_arr))


# test min_element
@pytest.mark.parametrize(
    "arg, expected",
    [
        [((3,), (2, 3, 4)), 2],
        [((4,), (1.0, 2.0, -3.0, 4.0)), -3.0],
        [((2, 3), (9, 10, 3, 4, 5, 6)), 3],
        [((2, 3), (9.0, -10.0, 3.0, 4.0, 5.0, 6.0)), -10.0]
    ]
)
def test_min_element(arg, expected):
    """
    Verify that smallest numeric of array is found
    """
    my_arr = Array(arg[0], *arg[1])
    assert my_arr.min_element() == expected
