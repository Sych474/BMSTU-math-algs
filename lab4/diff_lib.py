from collections import namedtuple
from math import e, log

Point = namedtuple('Table', ['x', 'y'])

def right_newton(table, h):
    der = [None for i in range(len(table))]
    for i in range(len(table)-1):
        der[i] = (table[i+1].y - table[i].y)/(table[i+1].x - table[i].x)
    return der


def middle_newton(table, h):
    der = [None for i in range(len(table))]
    for i in range(1, len(table)-1):
        #der[i] = (table[i+1].y - table[i-1].y)/(2*h)
        der[i] = (table[i+1].y - table[i-1].y)/(table[i+1].x - table[i-1].x)
    return der


def high_precision(table, h):
    der = [None for i in range(len(table))]
    n = len(table)-1
    der[0] = (-3*table[0].y + 4*table[1].y - table[2].y)/(table[2].x - table[0].x)
    der[n] = (3 * table[n].y - 4 * table[n-1].y + table[n-2].y) / (table[n].x - table[n-2].x)
    #der[0] = (-3*table[0].y + 4*table[1].y - table[2].y)/(2*h)
    #der[n] = (3 * table[n].y - 4 * table[n-1].y + table[n-2].y) / (2*h)
    return der


def runge(table, h):
    h1 = [None for i in range(len(table))]
    for i in range(len(table) - 1):
        h1[i] = (table[i + 1].y - table[i].y) / (table[i+1].x - table[i].x)
        #h1[i] = (table[i + 1].y - table[i].y) / h
    for i in range(len(table) - 2, len(table)):
        h1[i] = (table[i].y - table[i - 1].y) / (table[i].x - table[i-1].x)
        #h1[i] = (table[i].y - table[i-1].y) / h

    h2 = [None for i in range(len(table))]
    for i in range(len(table) - 2):
        h2[i] = (table[i + 2].y - table[i].y) / (table[i+2].x - table[i].x)
        #h2[i] = (table[i + 2].y - table[i].y) / (2 * h)
    for i in range(len(table) - 2, len(table)):
        h2[i] = (table[i].y - table[i - 2].y) / (table[i].x - table[i-2].x)
        #h2[i] = (table[i].y - table[i - 2].y) / (2 * h)

    res = [None for i in range(len(table))]
    for i in range(len(table)):
        res[i] = h1[i] + (h1[i] - h2[i])

    return res


def alignment_variables(table, h):
    tmp_table = [Point(elem.x, log(elem.y)) for elem in table]
    ans = [None for i in range(len(tmp_table))]
    for i in range(1, len(tmp_table) - 1):
        #h2 = 2 * h
        h2 = tmp_table[i + 1].x - tmp_table[i - 1].x
        ans[i] = (tmp_table[i + 1].y - tmp_table[i - 1].y) / (h2) * table[i].y
    return ans