import pytest
from typing import List, Tuple
from app.main import add, reduce_vectors

# Define type aliases explicitly for test clarity
Vector2DInt = Tuple[int, int]
Vector2DFloat = Tuple[float, float]

"""
What These Tests Cover
✔ Integer and floating-point addition with add()
✔ Edge cases (negative numbers, zeros, large values)
✔ Using reduce_vectors() to process a list of tuples
✔ Ensuring an empty list returns an empty list
"""

@pytest.mark.parametrize(
    "vector, expected",
    [
        ((2, 3), 5),
        ((-1, -5), -6),
        ((0, 10), 10),
        ((1000000, 2000000), 3000000),
    ],
)
def test_add_int(vector: Vector2DInt, expected: int):
    assert add(vector) == expected


@pytest.mark.parametrize(
    "vector, expected",
    [
        ((2.5, 3.5), 6.0),
        ((-1.1, -2.2), pytest.approx(-3.3)),  # ✅ Use pytest.approx() for floating-point values
        ((0.0, 7.3), pytest.approx(7.3)),
    ],
)
def test_add_float(vector: Vector2DFloat, expected: float):
    assert add(vector) == expected


@pytest.mark.parametrize(
    "vectors, expected",
    [
        ([(1, 2), (3, 4), (5, 6)], [3, 7, 11]),
        [( (-1, 1), (-2, 2), (-3, 3)), [0, 0, 0]],
        ([(10, 20), (30, 40), (50, 60)], [30, 70, 110]),
    ],
)
def test_reduce_vectors_int(vectors: List[Vector2DInt], expected: List[int]):
    assert reduce_vectors(vectors, add) == expected


@pytest.mark.parametrize(
    "vectors, expected",
    [
        ([(1.5, 2.5), (3.1, 4.2), (5.7, 6.3)], pytest.approx([4.0, 7.3, 12.0])),  # ✅ Use pytest.approx()
        ([(0.0, 0.0), (0.1, 0.2), (-1.5, 1.5)], pytest.approx([0.0, 0.3, 0.0])),
    ],
)
def test_reduce_vectors_float(vectors: List[Vector2DFloat], expected: List[float]):
    assert reduce_vectors(vectors, add) == expected


def test_reduce_vectors_empty():
    assert reduce_vectors([], add) == []

