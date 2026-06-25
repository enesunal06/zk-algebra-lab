class FieldElement:
    """An element of the prime field F_p."""

    def __init__(self, value, prime):
        if prime <= 1:
            raise ValueError("prime must be greater than 1")

        self.value = value % prime
        self.prime = prime

    def _check_same_field(self, other):
        if self.prime != other.prime:
            raise ValueError("cannot operate on elements from different fields")

    def __eq__(self, other):
        if not isinstance(other, FieldElement):
            return False

        return self.value == other.value and self.prime == other.prime

    def __add__(self, other):
        self._check_same_field(other)
        # Addition in F_p: (a + b) mod p.
        return FieldElement(self.value + other.value, self.prime)

    def __sub__(self, other):
        self._check_same_field(other)
        # Subtraction in F_p: (a - b) mod p.
        return FieldElement(self.value - other.value, self.prime)

    def __neg__(self):
        # Additive inverse in F_p: -a mod p.
        return FieldElement(-self.value, self.prime)

    def __mul__(self, other):
        self._check_same_field(other)
        # Multiplication in F_p: (a * b) mod p.
        return FieldElement(self.value * other.value, self.prime)

    def __pow__(self, exponent):
        # Negative powers are defined using the multiplicative inverse.
        if exponent < 0:
            return self.inverse() ** (-exponent)

        # Modular exponentiation: a^n mod p.
        return FieldElement(pow(self.value, exponent, self.prime), self.prime)

    def inverse(self):
        if self.value == 0:
            raise ZeroDivisionError("zero has no multiplicative inverse")

        # By Fermat's little theorem: a^(p-1) = 1 mod p,
        # so a^(-1) = a^(p-2) mod p for a != 0.
        return FieldElement(pow(self.value, self.prime - 2, self.prime), self.prime)

    def __truediv__(self, other):
        self._check_same_field(other)
        # Division in F_p is multiplication by the inverse.
        return self * other.inverse()

    def __repr__(self):
        return f"FieldElement({self.value} mod {self.prime})"
