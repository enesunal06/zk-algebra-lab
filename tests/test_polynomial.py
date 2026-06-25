import pytest

from zk_algebra.field import FieldElement
from zk_algebra.polynomial import Polynomial


def test_polynomial_stores_coefficients() -> None:
    p = 17

    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(5, p),
    ])

    assert f.coefficients == (
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(5, p),
    )


def test_trailing_zero_coefficients_are_removed() -> None:
    p = 17

    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(0, p),
        FieldElement(0, p),
    ])

    assert f.coefficients == (
        FieldElement(3, p),
        FieldElement(2, p),
    )
    assert f.degree() == 1


def test_zero_polynomial_keeps_one_zero_coefficient() -> None:
    p = 17

    f = Polynomial([
        FieldElement(0, p),
        FieldElement(0, p),
        FieldElement(0, p),
    ])

    assert f.coefficients == (FieldElement(0, p),)
    assert f.degree() == 0


def test_degree() -> None:
    p = 17

    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(5, p),
    ])

    assert f.degree() == 2


def test_prime() -> None:
    p = 17

    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
    ])

    assert f.prime() == 17


def test_evaluate_polynomial() -> None:
    p = 17

    # f(x) = 3 + 2x + 5x^2 over F_17
    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(5, p),
    ])

    x = FieldElement(4, p)

    # f(4) = 3 + 2*4 + 5*4^2 = 91 = 6 mod 17
    assert f.evaluate(x) == FieldElement(6, p)


def test_polynomial_cannot_be_empty() -> None:
    with pytest.raises(ValueError):
        Polynomial([])


def test_coefficients_must_be_in_same_field() -> None:
    with pytest.raises(ValueError):
        Polynomial([
            FieldElement(1, 17),
            FieldElement(2, 19),
        ])


def test_cannot_evaluate_outside_field() -> None:
    f = Polynomial([
        FieldElement(1, 17),
        FieldElement(2, 17),
    ])

    with pytest.raises(ValueError):
        f.evaluate(FieldElement(3, 19))


def test_polynomial_equality() -> None:
    p = 17

    f = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
        FieldElement(0, p),
    ])

    g = Polynomial([
        FieldElement(3, p),
        FieldElement(2, p),
    ])

    assert f == g
