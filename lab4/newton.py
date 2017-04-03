from collections import namedtuple

Point = namedtuple('Table', ['x', 'y'])

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