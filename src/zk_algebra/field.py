from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache


@lru_cache(maxsize=None)
def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Trial division up to sqrt(n) is enough to confirm primality.
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


@dataclass(frozen=True)
class FieldElement:
    """An element of the prime field F_p."""

    value: int
    prime: int

    def __post_init__(self) -> None:
        if self.prime <= 1:
            raise ValueError("prime must be greater than 1")
        if not _is_prime(self.prime):
            raise ValueError(f"{self.prime} is not prime, F_p requires a prime modulus")

        # Store the canonical representative in {0, 1, ..., p-1}.
        object.__setattr__(self, "value", self.value % self.prime)

    def _check_same_field(self, other: FieldElement) -> None:
        if self.prime != other.prime:
            raise ValueError("cannot operate on elements from different fields")

    def __add__(self, other: FieldElement) -> FieldElement:
        self._check_same_field(other)
        # Addition in F_p: (a + b) mod p.
        return FieldElement(self.value + other.value, self.prime)

    def __sub__(self, other: FieldElement) -> FieldElement:
        self._check_same_field(other)
        # Subtraction in F_p: (a - b) mod p.
        return FieldElement(self.value - other.value, self.prime)

    def __neg__(self) -> FieldElement:
        # Additive inverse in F_p: -a mod p.
        return FieldElement(-self.value, self.prime)

    def __mul__(self, other: FieldElement) -> FieldElement:
        self._check_same_field(other)
        # Multiplication in F_p: (a * b) mod p.
        return FieldElement(self.value * other.value, self.prime)

    def __pow__(self, exponent: int) -> FieldElement:
        # Negative powers are defined via the multiplicative inverse:
        # a^(-n) = (a^(-1))^n. inverse() raises ZeroDivisionError for a=0,
        # which is correct since 0^(-n) is undefined.
        if exponent < 0:
            return self.inverse() ** (-exponent)

        # Modular exponentiation: a^n mod p.
        return FieldElement(pow(self.value, exponent, self.prime), self.prime)

    def inverse(self) -> FieldElement:
        if self.value == 0:
            raise ZeroDivisionError("zero has no multiplicative inverse")

        # By Fermat's little theorem: a^(p-1) = 1 mod p,
        # so a^(-1) = a^(p-2) mod p for a != 0.
        return FieldElement(pow(self.value, self.prime - 2, self.prime), self.prime)

    def __truediv__(self, other: FieldElement) -> FieldElement:
        self._check_same_field(other)
        # Division in F_p is multiplication by the inverse.
        return self * other.inverse()

    def __repr__(self) -> str:
        return f"FieldElement({self.value} mod {self.prime})"
