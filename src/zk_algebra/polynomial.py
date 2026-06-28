from zk_algebra.field import FieldElement


class Polynomial:
    def __init__(self, coefficients):
        if not coefficients:
            raise ValueError("polynomial must have at least one coefficient")

        # Remove trailing zero coefficients.
        # Example: 3 + 2x + 0x^2 is the same polynomial as 3 + 2x.
        cleaned_coefficients = list(coefficients)
        while len(cleaned_coefficients) > 1 and cleaned_coefficients[-1].value == 0:
            cleaned_coefficients.pop()
        # All coefficients must belong to the same field F_p.
        prime = cleaned_coefficients[0].prime
        for coefficient in cleaned_coefficients:
            if coefficient.prime != prime:
                raise ValueError("all coefficients must belong to the same field")

        self.coefficients = tuple(cleaned_coefficients)

    def prime(self):
        return self.coefficients[0].prime

    def degree(self):
        # we assign degree 0 to the zero polynomial for simplicity.
        return len(self.coefficients) - 1

    def evaluate(self, x):
        if x.prime != self.prime():
            raise ValueError("cannot evaluate polynomial outside its field")

        # Horner's method
        # Ex: a0 + a1*x + a2*x^2 = ((a2*x) + a1)*x + a0
        result = FieldElement(0, self.prime())

        for coefficient in reversed(self.coefficients):
            result = result * x + coefficient

        return result

    def _check_same_field(self, other):
        if self.prime() != other.prime():
            raise ValueError("cannot operate on polynomials over different fields")

    def __add__(self, other):
        self._check_same_field(other)

        max_length = max(len(self.coefficients), len(other.coefficients))
        zero = FieldElement(0, self.prime())
        result = []

        for i in range(max_length):
            a = self.coefficients[i] if i < len(self.coefficients) else zero
            b = other.coefficients[i] if i < len(other.coefficients) else zero
            result.append(a + b)

        return Polynomial(result)

    def __sub__(self, other):
        self._check_same_field(other)

        max_length = max(len(self.coefficients), len(other.coefficients))
        zero = FieldElement(0, self.prime())
        result = []

        for i in range(max_length):
            a = self.coefficients[i] if i < len(self.coefficients) else zero
            b = other.coefficients[i] if i < len(other.coefficients) else zero
            result.append(a - b)

        return Polynomial(result)

    def __mul__(self, other):
        self._check_same_field(other)

        zero = FieldElement(0, self.prime())
        result_length = self.degree() + other.degree() + 1
        result = [zero for _ in range(result_length)]

        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):
                result[i + j] = result[i + j] + (a * b)

        return Polynomial(result)

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False

        return self.coefficients == other.coefficients

    def __repr__(self):
        return f"Polynomial({self.coefficients})"
