# MIT License
# 
# Copyright (c) 2023-2024 Jack Stout
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" A set of functions for manipulating bits.

These functions accept iterables containing bits.
A bit is represented by a zero (0) or a one (1).
Iterables are treated as big-endian.

>>> a = [1, 1, 0, 0, 0, 1, 0, 1]
>>> b = [0, 0, 0, 1, 0, 1, 1, 0]

>>> op_add(a, b)
(1, 1, 0, 1, 1, 0, 1, 1)

>>> op_xor(a, b)
(1, 1, 0, 1, 0, 0, 1, 1)

>>> op_neg(a)
(0, 0, 1, 1, 1, 0, 1, 0)

"""

version = "v1.0.1"
version_iterable = [1, 0, 1]

import inspect


# -- Basic Operations --

def op_and(*args):
    """Output[i] is 1 if all arg[i] equal 1, else 0."""
    _ensure_min_arg_count(2, *args)
    _ensure_same_arg_length(*args)
    accumulator = [1] * len(args[0])
    for arg in args:
        accumulator = [accumulator[i] & arg[i] for i in range(len(arg))]
    return tuple(accumulator)

def op_or(*args):
    """Output[i] is 1 if any arg[i] equals 1, else 0."""
    _ensure_min_arg_count(2, *args)
    _ensure_same_arg_length(*args)
    accumulator = [0] * len(args[0])
    for arg in args:
        accumulator = [accumulator[i] | arg[i] for i in range(len(arg))]
    return tuple(accumulator)

def op_xor(*args):
    """Output[i] is 1 if exactly one arg[i] equals 1, else 0."""
    _ensure_min_arg_count(2, *args)
    _ensure_same_arg_length(*args)
    counter = [0] * len(args[0])
    for arg in args:
        counter = [counter[i] + arg[i] for i in range(len(arg))]
    accumulator = [{True: 1, False: 0}[bit == 1] for bit in counter]
    return tuple(accumulator)

def op_neg(bits):
    """Return bitwise complement of bits as tuple."""
    new_bits = [(bit + 1) % 2 for bit in bits]
    return tuple(new_bits)

def op_ls0(shift, bits):
    """Left-shift bits. Fill new bits with 0."""
    if shift < 1:
        raise ValueError("shift must be greater than 0 (given {})".format(shift))
    length = len(bits)
    retainer_length = max(length - shift, 0)
    accumulator = [0] * len(bits)
    accumulator[:retainer_length] = bits[shift:]
    return tuple(accumulator)

def op_ls1(shift, bits):
    """Left-shift bits. Fill new bits with 1."""
    if shift < 1:
        raise ValueError("shift must be greater than 0 (given {})".format(shift))
    length = len(bits)
    retainer_length = max(length - shift, 0)
    accumulator = [1] * len(bits)
    accumulator[:retainer_length] = bits[shift:]
    return tuple(accumulator)

def op_rs0(shift, bits):
    """Right-shift bits. Fill new bits with 0."""
    if shift < 1:
        raise ValueError("shift must be greater than 0 (given {})".format(shift))
    length = len(bits)
    retainer_length = max(length - shift, 0)
    accumulator = [0] * len(bits)
    accumulator[shift:] = bits[:retainer_length]
    return tuple(accumulator)

def op_rs1(shift, bits):
    """Right-shift bits. Fill new bits with 1."""
    if shift < 1:
        raise ValueError("shift must be greater than 0 (given {})".format(shift))
    length = len(bits)
    retainer_length = max(length - shift, 0)
    accumulator = [1] * len(bits)
    accumulator[shift:] = bits[:retainer_length]
    return tuple(accumulator)


# -- Math Operations --

def op_add(*args):
    """Return sum of args in tuple of same length."""
    _ensure_min_arg_count(2, *args)
    _ensure_same_arg_length(*args)
    accumulator = [0] * len(args[0])
    for addend in args:
        accumulator = _add_two_values(accumulator, addend)
    return tuple(accumulator)

def op_sub(*args):
    """Return difference of args in tuple of same length.

    When given more than two arguments, holds the first value. The sum
    of all remaining values is then subtracted from the first.
    """
    _ensure_min_arg_count(2, *args)
    _ensure_same_arg_length(*args)
    accumulator = args[0]
    subtrahends = args[1:]
    if not subtrahends:
        return tuple(accumulator)
    for subtrahend in subtrahends:
        inverse = op_neg(subtrahend)
        addend = op_add(inverse, _one(len(inverse)))
        accumulator = op_add(accumulator, addend)
    return tuple(accumulator)

def op_inc(bits):
    """Adds 1."""
    accumulator = op_add(bits, _one(len(bits)))
    return tuple(accumulator)

def op_dec(bits):
    """Subtracts 1."""
    accumulator = op_sub(bits, _one(len(bits)))
    return tuple(accumulator)


# -- Internal utilities --

def _one(length):
    accumulator = [0] * (length - 1) + [1]
    return tuple(accumulator)

def _ensure_min_arg_count(min_count, *args):
    if len(args) < min_count:
        raise TypeError(
            "{}() expects at least {} arguments (given {})"
            "".format(_parent_function_name(), min_count, len(args))
        )

def _parent_function_name(depth=1):
    return inspect.stack()[depth+1][3]

def _ensure_same_arg_length(*args):
    """If all args have same length, exit cleanly. Else, raise TypeError."""
    l = [len(arg) for arg in args]
    s = set(l)
    if len(s) == 1:
        return
    else:
        raise TypeError(
            "{}() requires arguments to have same length (lengths given: {})"
            "".format(_parent_function_name(), l)
        )

def _add_two_values(a, b):
    """Return sum of a and b as tuple."""
    assert len(a) == len(b)
    carry = 0
    out = []
    for i in range(len(a)):
        index = -(i+1)
        total = a[index] + b[index] + carry
        out.insert(0, total % 2)
        if total > 1:
            carry = 1
        else:
            carry = 0
    return tuple(out)
