from random import randint
from collections import namedtuple

Point = namedtuple('Table', ['x', 'y', 'p'])


def fi(x, k):
    return x**k


def get_table(filename):
    table = []
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            x, y, p = map(float, line.split())
            table.append(Point(x, y, p))
            line = f.readline()
    table.sort()
    return table


def print_plot(table, A , n):
    import matplotlib.pyplot as plt
    import numpy as nmp
    dx = 10
    if len(table) > 1:
        dx = (table[1].x - table[0].x)

    x = nmp.linspace(table[0].x - dx, table[-1].x + dx, 100)
    y = [0 for i in range(len(x))]
    for i in range(len(x)):
        for j in range(n+1):
            y[i] += fi(x[i], j) * A[j]

    plt.plot(x, y)
    x1 = [point.x for point in table]
    y1 = [point.y for point in table]

    plt.plot(x1, y1, 'kD', color='red', label='$Исходная таблица$')
    plt.grid(True)

    plt.show()


def get_slau(table, n):
    N = len(table)
    A = [[0 for i in range(n+1)]for j in range(n+1)]
    B = [0 for i in range(n+1)]
    for m in range(n+1):
        for i in range(N):
            tmp = table[i].p * fi(table[i].x, m)
            for k in range(n+1):
                A[m][k] += tmp * fi(table[i].x, k)
            B[m] += tmp * table[i].y
    return A, B


def get_reverse(matrix):
    n = len(matrix)
    A = [[matrix[j][i] for i in range(n)]for j in range(n)]
    rev = [[1 if (i == j) else 0 for i in range(n)]for j in range(n)]

    #прямой ход
    for i in range(n):
        if A[i][i] == 0:
            for j in range(i+1, n):
                if A[j][j] != 0:
                    A[i], A[j] = A[j], A[i]
                    rev[i], rev[j] = rev[j], rev[i]
                    break
        for j in range(i+1, n):
            mult = A[j][i]/A[i][i]
            for k in range(n):
                A[j][k] -= A[i][k] * mult
                rev[j][k] -= rev[i][k] * mult
    #обратный ход
    for i in range(n-1, -1, -1):
        if A[i][i] == 0:
            for j in range(i - 1, -1, -1):
                if A[j][j] != 0:
                    A[i], A[j] = A[j], A[i]
                    rev[i], rev[j] = rev[j], rev[i]
                    break
        for j in range(i - 1, -1, -1):
            mult = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= A[i][k] * mult
                rev[j][k] -= rev[i][k] * mult
    for i in range(n):
        for j in range(n):
            rev[i][j] /= A[i][i]
    return rev


def mult(col, matr):
    n = len(col)
    res = [0 for j in range(n)]
    for j in range(n):
        for k in range(n):
            res[j] += col[k] * matr[j][k]
    return res


def get_aproximation_array(table , n):
    m, b = get_slau(table, n)
    print(b)
    print(m)
    m_rev = get_reverse(m)
    a_arr = mult(b, m_rev)
    print(a_arr)
    return a_arr

from math import sin


def f(x):
    return sin(x)


def f1(x):
    return x*x


def prepare_table(filename, f, a, b, dx, delta):
    with open(filename, "w") as file:
        x = a
        while x <= b:
            y = f(x) + randint(-100, 100)/200 * delta
            p = 1
            print("{:7.3f} {:7.3f} {:7.3f}".format(x, y, p), file=file)
            x += dx


def print_table(table):
    print(" "*6+"x"+" "*7+"y"+" "*7+"p")
    for line in table:
        print("{:7.3f} {:7.3f} {:7.3f}".format(line.x, line.y, line.p))

prepare_table(filename="t2.txt", f=f1, a=-2.5, b=2.5, dx=0.1, delta=3)
table = get_table("table.txt")
print_table(table)
n = int(input("Введите степень полинома: "))
if n+1 > len(table):
    print("В таблице недостаточно точек")
else:
    A = get_aproximation_array(table, n)
    print_plot(table, A, n)