from math import e
from collections import namedtuple

Point = namedtuple('Table', ['x', 'y'])


def f(x):
    return e**x


def right_newton(table, h):
    der = [None for i in range(len(table))]
    for i in range(len(table)-1):
        der[i] = (table[i+1].y - table[i].y)/h
    return der


def middle_newton(table, h):
    der = [None for i in range(len(table))]
    for i in range(1, len(table)-1):
        der[i] = (table[i+1].y - table[i-1].y)/(2*h)
    return der


def high_precision(table, h):
    der = [None for i in range(len(table))]
    n = len(table)-1
    der[0] = (-3*table[0].y + 4*table[1].y - table[2].y)/(2*h)
    der[n] = (3 * table[n].y - 4 * table[n-1].y + table[n-2].y) / (2*h)
    return der


def get_table(f, a, b, h):
    table = list()
    x = a
    while x <= b:
        table.append(Point(x, f(x)))
        x += h
    return table


def print_table(table, r_newton, m_newton, h_perc):
    print("|{:7s}|{:7s}|{:7s}|{:7s}|{:7s}|".format("x", "y", "right", "middle", "high"))
    for i in range(len(table)):
        s1 = "{:7.4f}".format(r_newton[i]) if r_newton[i] else ' '
        s2 = "{:7.4f}".format(m_newton[i]) if m_newton[i] else ' '
        s3 = "{:7.4f}".format(h_perc[i]) if h_perc[i] else ' '
        print("|{:7.4f}|{:7.4f}|{:7s}|{:7s}|{:7s}|".format(table[i].x, table[i].y, s1, s2, s3))





def main():
    a = 1
    b = 3
    #h = float(input("Введите шаг: "))
    h = 0.5
    table = get_table(f=f, a=a, b=b, h=h)
    r_n = right_newton(table=table, h=h)
    m_n = middle_newton(table=table, h=h)
    h_p = high_precision(table=table, h=h)
    print_table(table=table, r_newton=r_n, m_newton=m_n, h_perc=h_p)


if __name__ == '__main__':
    main()
