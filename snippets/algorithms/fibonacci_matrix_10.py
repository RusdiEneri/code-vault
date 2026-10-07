def fib_matrix(n):
    if n <= 1: return n
    def multiply(A, B):
        return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]
    def power(M, p):
        res = [[1, 0], [0, 1]]
        base = M
        while p > 0:
            if p % 2 == 1: res = multiply(res, base)
            base = multiply(base, base)
            p //= 2
        return res
    F = [[1, 1], [1, 0]]
    return power(F, n - 1)[0][0]
