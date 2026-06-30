import pytest

from zk_algebra.field import FieldElement
from zk_algebra.interpolation import lagrange_interpolate
from zk_algebra.polynomial import Polynomial


def test_lagrange_interpolation_recovers_quadratic() -> None:
    p = 17

    points = [
        (FieldElement(1, p), FieldElement(6, p)),
        (FieldElement(2, p), FieldElement(11, p)),
        (FieldElement(3, p), FieldElement(1, p)),
    ]

    f = lagrange_interpolate(points)

    # The recovered polynomial is f(x) = 3 + 2x + x^2 over F_17.
    assert f == Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(1, p),
    ])


def test_interpolated_polynomial_matches_all_input_points() -> None:
    p = 17

    points = [
        (FieldElement(1, p), FieldElement(6, p)),
        (FieldElement(2, p), FieldElement(11, p)),
        (FieldElement(3, p), FieldElement(1, p)),
    ]

    f = lagrange_interpolate(points)

    for x, y in points:
        assert f.evaluate(x) == y


def test_lagrange_interpolation_with_single_point() -> None:
    p = 17

    points = [
        (FieldElement(5, p), FieldElement(9, p)),
    ]

    f = lagrange_interpolate(points)

    assert f == Polynomial([FieldElement(9, p)])
    assert f.evaluate(FieldElement(5, p)) == FieldElement(9, p)


def test_lagrange_interpolation_requires_at_least_one_point() -> None:
    with pytest.raises(ValueError):
        lagrange_interpolate([])


def test_lagrange_interpolation_requires_same_field() -> None:
    points = [
        (FieldElement(1, 17), FieldElement(2, 17)),
        (FieldElement(2, 17), FieldElement(3, 19)),
    ]

    with pytest.raises(ValueError):
        lagrange_interpolate(points)


def test_lagrange_interpolation_requires_distinct_x_values() -> None:
    p = 17

    points = [
        (FieldElement(1, p), FieldElement(2, p)),
        (FieldElement(1, p), FieldElement(3, p)),
    ]

    with pytest.raises(ValueError):
        lagrange_interpolate(points)
