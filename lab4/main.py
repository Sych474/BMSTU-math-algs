from math import e
from collections import namedtuple

Point = namedtuple('Table', ['x', 'y'])


def f(x):
    return e**x


def get_table(f, a, b, h):
    table = list()
    x = a
    while x <= b:
        table.append(Point(x, f(x)))
        x += h
    return table


def print_table(table):
    print("|{:7s}|{:7s}|".format("x", "y"))
    for line in table:
        print("|{:7.4f}|{:7.4f}|".format(line.x, line.y))


def main():
    a = 1
    b = 3
    h = float(input("Введите шаг: "))
    table = get_table(f=f, a=a, b=b, h=h)
    print_table(table=table)


if __name__ == '__main__':
    main()
