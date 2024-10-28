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

Operations              | Function names   | Example
----------------------- | ---------------- | ----------------------------------
And                     | `op_and`         | `op_and([1, 1], [0, 1]) => (0, 1)`
Or                      | `op_or`          | `op_or([1, 1], [0, 1]) => (1, 1)`
Xor                     | `op_xor`         | `op_xor([1, 1], [0, 1]) => (1, 0)`
Complement              | `op_neg`         | `op_neg([1, 0]) => (0, 1)`
Left shift (fill zero)  | `op_ls0`         | `op_ls0([1, 1]) => (1, 0)`
Left shift (fill one)   | `op_ls1`         | `op_ls1([0, 0]) => (0, 1)`
Right shift (fill zero) | `op_rs0`         | `op_rs0([1, 1]) => (0, 1)`
Right shift (fill one)  | `op_rs1`         | `op_rs1([0, 0]) => (1, 0)`
Add                     | `op_add`         | `op_add([0, 1], [0, 1]) => (1, 0)`
Subtract                | `op_sub`         | `op_sub([1, 1], [0, 1]) => (0, 1)`
Increment               | `op_inc`         | `op_inc([1, 0]) => (1, 1)`
Decrement               | `op_dec`         | `op_dec([1, 0]) => (0, 1)`
