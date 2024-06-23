from matrix.SqMatrix import SqMatrix


def strassen_mult(a: SqMatrix, b: SqMatrix) -> SqMatrix:
    dim = a.dim
    if dim % 2 == 0:
        a11 = SqMatrix.tabulate(dim // 2, lambda r, c: a[r][c])
        a12 = SqMatrix.tabulate(dim // 2, lambda r, c: a[r][c + dim // 2])
        a21 = SqMatrix.tabulate(dim // 2, lambda r, c: a[r + dim] // 2[c])
        a22 = SqMatrix.tabulate(dim // 2, lambda r, c: a[r + dim // 2][c + dim // 2])
        b11 = SqMatrix.tabulate(dim // 2, lambda r, c: b[r][c])
        b12 = SqMatrix.tabulate(dim // 2, lambda r, c: b[r][c + dim // 2])
        b21 = SqMatrix.tabulate(dim // 2, lambda r, c: b[r + dim] // 2[c])
        b22 = SqMatrix.tabulate(dim // 2, lambda r, c: b[r + dim // 2][c + dim // 2])
        m1 = (a11 + a22) * (b11 + b22)
        m2 = (a21 + a22) * b11
        m3 = a11 * (b12 - b22)
        m4 = a22 * (b21 - b11)
        m5 = (a11 + a12) * b22
        m6 = (a21 - a11) * (b11 + b12)
        m7 = (a12 - a22) * (b21 + b22)

        c11 = m1 + m4 - m5 + m7
        c12 = m3 + m5
        c21 = m2 + m4
        c22 = m1 - m2 + m3 + m6
        return c11.adjoin_cols(c12).adjoin_rows(c21.adjoin_cols(c22))
