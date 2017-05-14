"""
Нахождение верхнего передела интегрирования по заданной функции и значению интеграла
интеграл вычисляется методом Гаусса с помощью составление квадратурной формулы Гаусса
по корням полинома Лежандра заданной степени
"""
from math import sqrt, pi, e, cos


EPS = 10**-10


def P(n, x):
    if n == 0:
        return 1
    if n == 1:
        return x

    p1, p2 = 1, x
    c_n = 1
    while c_n < n:
        p1, p2 = p2, (2 * c_n + 1) / (c_n + 1) * x * p2 - c_n / (c_n + 1) * p1
        c_n += 1
    return p2


def P2(n, x):
    if n == 0:
        return 1
    if n == 1:
        return x

    return (2*(n-1)+1)/((n-1)+1) * x * P(n-1, x) - (n-1)/((n-1)+1) * P(n-2, x)


def P_derivative(n, x):
    return n / (1 - x*x) * (P(n-1, x) - x*P(n, x))


def binp(a, b, f):
    eps = EPS * abs(b - a)
    if f(a) < f(b):
        low, up = a, b
    else:
        low, up = b, a

    while abs(up - low) > eps:
        mid = (low + up) / 2
        if f(mid) > 0:
            up = mid
        else:
            low = mid
    return up


def legendre_roots2(n):
    roots = list()
    count = 0
    step = 2/n
    intervals = list()
    while count != n:
        count, curr = 0, -1
        while curr <= 1:
            if P(n=n, x=curr) * P(n=n, x=curr+step) < 0:
                count += 1
                intervals.append((curr, curr+step))
            curr += step
        if count != n:
            step /= 2
            intervals.clear()

    def f(x):
        return P(n, x)

    for interval in intervals:
        roots.append(binp(a=interval[0], b=interval[1], f=f))

    return roots


def legendre_roots(n):
    roots = list()

    for i in range(1, n+1):
        x_old = cos(pi*(4*i - 1)/(4*n + 2))
        x_start = x_old
        x_new = x_old - P(n=n, x=x_old)/P_derivative(n=n, x=x_old)

        while abs(x_new - x_old)/x_start > EPS:
            x_old, x_new = x_new, x_new - P(n=n, x=x_new)/P_derivative(n=n, x=x_new)

        roots.append(x_new)
    return roots


def solve_matrix(A, B):
    n = len(A)
    #прямой ход
    for i in range(n):
        if abs(A[i][i]) < EPS:
            for j in range(i+1, n):
                if abs(A[j][j]) > EPS:
                    A[i], A[j] = A[j], A[i]
                    B[i], B[j] = B[j], B[i]
                    break
        for j in range(i+1, n):
            mult = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= A[i][k] * mult
            B[j] -= B[i] * mult
    #обратный ход
    for i in range(n-1, -1, -1):
        if abs(A[i][i]) < EPS:
            for j in range(i - 1, -1, -1):
                if abs(A[j][j]) > EPS:
                    A[i], A[j] = A[j], A[i]
                    B[i], B[j] = B[j], B[i]
                    break
        for j in range(i - 1, -1, -1):
            mult = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= A[i][k] * mult
            B[j] -= B[i] * mult
    for i in range(n):
        B[i] /= A[i][i]
    return B


def gauss_integral(a, b, f, n):
    #import numpy
    t = legendre_roots2(n=n)
    #t1 = legendre_roots2(n=n)

    #print("Корни: ", t)
    #print("Корни: ", t1)
    A = [0 if k % 2 == 1 else 2/(k+1) for k in range(n)]
    #print(A)
    matr = [[t[i]**k for i in range(n)] for k in range(n)]
    #print(matr)
    #B = numpy.linalg.solve(matr, A)
    A = solve_matrix(matr, A)
    #print(B)
    #print("Коэфиценты: ", A)
    res = 0
    d = (b - a)/2
    s = (a + b)/2
    for i in range(n):
        res += A[i] * f(d * t[i] + s)

    return res * d


def ft(t):
    return e ** (-t*t/2)


def get_integral(x, n):
    return 1/sqrt(2*pi) * gauss_integral(a=0, b=x, f=ft, n=n)


def print_plot(a, b, f, point):
    import matplotlib.pyplot as plt
    import numpy as nmp

    x = nmp.linspace(a, b, 200)
    y = [f(x[i]) for i in range(len(x))]
    plt.plot(x, y)
    plt.plot(point, f(point), 'kD', color='red')

    plt.grid(True)
    plt.show()


def main():
    print(P(x=4, n=4))
    print(P2(x=4, n=4))

    a = float(input("Введите a: "))
    n = int(input("Введите n: "))

    def F(x):
        return get_integral(x=x, n=n) - a

    low, up = 0, 10
    eps = (up - low) * EPS
    while abs(up - low) > eps:
        mid = (low + up) / 2
        if F(mid) < 0:
            low = mid
        else:
            up = mid

    print("x =", up)
    print("Отклонение:", F(up))
    #print_plot(a=0, b=10, f=F, point=up)


if __name__ == '__main__':
    main()
