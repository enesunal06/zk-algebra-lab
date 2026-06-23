import pytest

from zk_algebra.field import FieldElement


def test_values_are_reduced_mod_prime() -> None:
    assert FieldElement(20, 17) == FieldElement(3, 17)
    assert FieldElement(-1, 17) == FieldElement(16, 17)


def test_addition() -> None:
    a = FieldElement(15, 17)
    b = FieldElement(5, 17)

    assert a + b == FieldElement(3, 17)


def test_subtraction() -> None:
    a = FieldElement(15, 17)
    b = FieldElement(5, 17)

    assert a - b == FieldElement(10, 17)


def test_negation() -> None:
    a = FieldElement(5, 17)

    assert -a == FieldElement(12, 17)


def test_multiplication() -> None:
    a = FieldElement(15, 17)
    b = FieldElement(5, 17)

    assert a * b == FieldElement(7, 17)


def test_inverse() -> None:
    b = FieldElement(5, 17)

    assert b.inverse() == FieldElement(7, 17)
    assert b * b.inverse() == FieldElement(1, 17)


def test_division() -> None:
    a = FieldElement(15, 17)
    b = FieldElement(5, 17)

    assert a / b == FieldElement(3, 17)


def test_positive_power() -> None:
    a = FieldElement(3, 17)

    assert a**4 == FieldElement(13, 17)


def test_negative_power() -> None:
    a = FieldElement(15, 17)

    assert a**-1 == FieldElement(8, 17)


def test_zero_has_no_inverse() -> None:
    zero = FieldElement(0, 17)

    with pytest.raises(ZeroDivisionError):
        zero.inverse()

    with pytest.raises(ZeroDivisionError):
        zero**-1


def test_different_fields_cannot_be_mixed() -> None:
    a = FieldElement(3, 17)
    b = FieldElement(3, 19)

    with pytest.raises(ValueError):
        a + b

    with pytest.raises(ValueError):
        a * b


def test_modulus_must_be_prime() -> None:
    with pytest.raises(ValueError):
        FieldElement(3, 1)

    with pytest.raises(ValueError):
        FieldElement(3, 15)