# BITOPS

A set of functions for manipulating bits.

These functions accept iterables containing bits.
A bit is represented by a zero (0) or a one (1).
Iterables are treated as big-endian.

```python
>>> a = [1, 1, 0, 0, 0, 1, 0, 1]
>>> b = [0, 0, 0, 1, 0, 1, 1, 0]

>>> op_add(a, b)
(1, 1, 0, 1, 1, 0, 1, 1)

>>> op_xor(a, b)
(1, 1, 0, 1, 0, 0, 1, 1)

>>> op_neg(a)
(0, 0, 1, 1, 1, 0, 1, 0)
```