from math import e, log
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


def runge(table, h):
    h_list = middle_newton(table, h)
    h2_list = [None for i in range(len(table))]
    for i in range(2, len(table) - 2):
        h2_list[i] = (table[i + 2].y - table[i - 2].y) / (4*h)
    res = [None for i in range(len(table))]
    for i in range(2, len(table) - 2):
        res[i] = h_list[i] + (h_list[i]-h2_list[i])/3
    return res


def alignment_variables(table, h):
    tmp_table = [Point(elem.x, log(elem.y)) for elem in table]
    ans = [None for i in range(len(tmp_table))]
    for i in range(1, len(tmp_table) - 1):
        ans[i] = (tmp_table[i + 1].y - tmp_table[i - 1].y) / (2 * h) * table[i].y
    return ans


def get_points_to_interpolation(point_list, x, n):
    # предполагается, что point_list отсортирован, и в нем как минимум n+1 точка
    x_ind = 0
    while x_ind < len(point_list) and point_list[x_ind].x < x:
        x_ind += 1
    lower_ind = x_ind - n // 2 - n % 2  # если нечетное, то вниз берем больше.
    upper_ind = x_ind + n // 2
    if lower_ind < 0:
        upper_ind += abs(lower_ind)
        lower_ind = 0
    elif upper_ind >= len(point_list):
        lower_ind -= upper_ind - (len(point_list) - 1)
        upper_ind = len(point_list) - 1
    return [point_list[i] for i in range(lower_ind, upper_ind + 1)]


def a_progression(a, b, n):
    return (a+b) *n // 2


def get_split_diffs(points_to_interpolation, n):
    split_diffs = [(points_to_interpolation[i].y if i < n+1 else 0)
                   for i in range(a_progression(a=1, b=n+1, n=n+1))]
    ind = n+1
    for i in range(n):
        offset = (n - 1 - i)
        for j in range(n-i):
            dy = split_diffs[ind - offset - 2] - split_diffs[ind - offset - 1]
            dx = points_to_interpolation[j].x - points_to_interpolation[j+i+1].x
            split_diffs[ind] = dy/dx
            ind += 1
    return split_diffs


def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def mult(combination):
    ans = 1
    for elem in combination:
        ans *= float(elem)
    return ans


def newton_polinom(table, x, n):
    if len(table) < n + 1:
        return None
    interp_points = get_points_to_interpolation(point_list=table, x=x, n=n)
    #print(interp_points)
    split_diffs = get_split_diffs(points_to_interpolation=interp_points, n=n)
    #print(split_diffs)
    z = [x - interp_points[i].x for i in range(len(interp_points))]
    #print(z)
    ind = n+1
    y = split_diffs[ind]
    for i in range(1, n):
        comb = combinations(z[:i+1], i)
        #comb_a = combinations([str(i) for i in range(i+1)], i)
        #for elem in comb_a:
        #    print(elem)

        ind += n - i + 1
        add = split_diffs[ind]
        tmp = 0
        for elem in comb:
        #    print(elem)
            tmp += mult(elem)
        #print(tmp)
        add *= tmp
        #print(add)
        y += add
    return y


def get_table(f, a, b, h):
    table = list()
    x = a
    while x <= b:
        table.append(Point(x, f(x)))
        x += h
    return table


def print_table(table, r_newton, m_newton, h_perc, runge, alignment):
    print("|{:10s}|{:10s}|{:10s}|{:10s}|{:10s}|{:10s}|{:10s}|".format("x", "y", "Правый", "Среднее", "Повыш.", "Рунге", "Выравн."))
    for i in range(len(table)):
        s1 = "{:10.4f}".format(r_newton[i]) if r_newton[i] else ' '
        s2 = "{:10.4f}".format(m_newton[i]) if m_newton[i] else ' '
        s3 = "{:10.4f}".format(h_perc[i]) if h_perc[i] else ' '
        s4 = "{:10.4f}".format(runge[i]) if runge[i] else ' '
        s5 = "{:10.4f}".format(alignment[i]) if alignment[i] else ' '
        print("|{:10.4f}|{:10.4f}|{:10s}|{:10s}|{:10s}|{:10s}|{:10s}|".format(table[i].x, table[i].y, s1, s2, s3, s4, s5))


def main():
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    h = float(input("Введите шаг: "))

    table = get_table(f=f, a=a, b=b, h=h)
    r_n = right_newton(table=table, h=h)
    m_n = middle_newton(table=table, h=h)
    h_p = high_precision(table=table, h=h)
    r = runge(table=table, h=h)
    a_v = alignment_variables(table=table, h=h)
    print_table(table=table, r_newton=r_n, m_newton=m_n, h_perc=h_p, runge=r, alignment=a_v)

    x = float(input("Введите x: "))
    n = int(input("Введите число узлов: "))
    print(newton_polinom(table=table, x=x, n=n-1))
    print()


if __name__ == '__main__':
    main()
