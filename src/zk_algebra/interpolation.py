from zk_algebra.field import FieldElement
from zk_algebra.polynomial import Polynomial


def lagrange_interpolate(points):
    if not points:
        raise ValueError("at least one point is required")

    prime = points[0][0].prime

    # All x and y values must belong to the same field F_p.
    for x, y in points:
        if x.prime != prime or y.prime != prime:
            raise ValueError("all points must belong to the same field")

    # The x-values must be distinct.
    # Otherwise, there is no unique interpolation polynomial.
    x_values = [x for x, _ in points]
    if len(set(x.value for x in x_values)) != len(x_values):
        raise ValueError("x-values must be distinct")

    zero = FieldElement(0, prime)
    one = FieldElement(1, prime)

    result = Polynomial([zero])

    for i, (x_i, y_i) in enumerate(points):
        # This will become the i-th Lagrange basis polynomial.
        basis = Polynomial([one])

        # This is the denominator:
        # (x_i - x_0)(x_i - x_1)... excluding j = i.
        denominator = one

        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue

            # Multiply the basis by (x - x_j).
            # As a coefficient list, x - x_j is [-x_j, 1].
            basis = basis * Polynomial([-x_j, one])

            # Accumulate the denominator evaluated at x_i.
            denominator = denominator * (x_i - x_j)

        # Field division is multiplication by the inverse in F_p.
        scalar = y_i / denominator

        # y_i * L_i(x)
        term = Polynomial([scalar]) * basis

        result = result + term

    return result
