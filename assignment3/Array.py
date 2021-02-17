#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys


class Array:
    # Assignment 3.3s
    def __init__(self, shape, *values):
        """
        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).
        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.
        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check whether all values are of the same (allowed) type
        allowed_dtypes = (int, float, bool)
        if type(values[0]) in allowed_dtypes:
            if not all(isinstance(val, type(values[0])) for val in values):
                raise ValueError(
                    "Values must be of the same data type")
        else:
            raise ValueError(
                "Values must be of either numeric or bool data type")

        # Check whether number of values match shape
        self.shape = shape
        dimprod = self.shape[0]
        for dim in range(1, len(self.shape)):
            dimprod *= self.shape[dim]
        if not dimprod == len(values):
            raise ValueError(
                "The number of values does not fit with the shape")

        # generate arrays
        self.flatten = list(values)
        self.array_dtype = type(self.flatten[0])
        if len(self.shape) == 1:
            # 1D array
            self.array = self.flatten[:]
        elif len(self.shape) == 2:
            # 2D array
            self.array = [list(values[i * self.shape[1]:self.shape[1] * (i + 1)])
                          for i in range(self.shape[0])]
        else:
            raise NotImplementedError(
                "Array class currently only supports 1D and 2D arrays")

    def __str__(self):
        """Returns a nicely printable string representation of the array.
        Returns:
            str: A string representation of the array.
        """

        return str(self.array)

    def __add__(self, other):
        """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """

        if not isinstance(other, (Array, int, float)):
            return NotImplemented

        if isinstance(other, (int, float)):
            new_values = tuple(e + other for e in self.flatten)
            return Array(self.shape, *new_values)

        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented
            else:
                new_values = tuple(
                    i + j for i, j in zip(self.flatten, other.flatten))
                return Array(self.shape, *new_values)

    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """

        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.
        Returns:
            Array: the difference as a new array.
        """

        if not isinstance(other, (Array, int, float)):
            return NotImplemented

        if isinstance(other, (int, float)):
            new_values = tuple(e - other for e in self.flatten)
            return Array(self.shape, *new_values)

        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented
            else:
                new_values = tuple(
                    i - j for i, j in zip(self.flatten, other.flatten))
                return Array(self.shape, *new_values)

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number being subtracted from.
        Returns:
            Array: the difference as a new array.
        """

        return Array(self.shape, *tuple(-e for e in self.flatten)).__add__(other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """

        if not isinstance(other, (Array, int, float)):
            return NotImplemented

        if isinstance(other, (int, float)):
            new_values = tuple(e * other for e in self.flatten)
            return Array(self.shape, *new_values)

        if isinstance(other, Array):
            if self.shape != other.shape:
                return NotImplemented
            else:
                new_values = tuple(
                    i * j for i, j in zip(self.flatten, other.flatten))
                return Array(self.shape, *new_values)

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """

        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.
        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.
        Args:
            other (Array): The array to compare with this array.
        Returns:
            bool: True if the two arrays are equal. False otherwise.
        """

        if not isinstance(other, (Array, int, float)):
            return False
        else:
            # Return True if arrays are identical, False if either not identical or shapes don't match
            return self.flatten == other.flatten

    def __getitem__(self, index):
        """Get the array entry at given index
        Args:
            index (int): The index of entry in array
        Returns:
            object (Array, float, int, bool): The entry in array
        """

        if isinstance(index, int):
            return self.array[index]
        else:
            raise ValueError("Index must be an integer")

    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.
        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        Args:
            other (Array, float, int): The array or number to compare with this array.
        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.
        Raises:
            ValueError: if the shape of self and other are not equal.
        """

        if isinstance(other, (int, float)):
            bool_values = tuple(e == other for e in self.flatten)
            return Array(self.shape, *bool_values)

        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Shape of arrays must be the same")
            else:
                """
                bool_values = tuple(True if i == j else False for i,
                                   j in zip(self.flatten, other.flatten))
                """
                bool_values = tuple(i == j for i, j in zip(
                    self.flatten, other.flatten))
                return Array(self.shape, *bool_values)

    def mean(self):
        """Computes the mean of the array
        Only needs to work for numeric data types.
        Returns:
            float: The mean of the array values.
        """

        return sum(self.flatten) / float(len(self.flatten))

    def variance(self):
        """Computes the variance of the array
        Only needs to work for numeric data types.
        The variance is computed as: mean((x - x.mean())**2)
        Returns:
            float: The variance of the array values.
        """

        return sum((e - self.mean())**2 for e in self.flatten) / len(self.flatten)

    def min_element(self):
        """Returns the smallest value of the array.
        Only needs to work for numeric data types.
        Returns:
            float: The value of the smallest element in the array.
        """

        return min(self.flatten)
