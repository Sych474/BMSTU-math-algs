def a_progression(a, b, n):
    return (a+b) *n // 2


def get_points_to_interpolation(point_list, x, n):
    # предполагается, что point_list отсортирован, и в нем как минимум n+1 точка
    x_ind = 0
    while x_ind < len(point_list) and point_list[x_ind][0] < x:
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


def get_split_diffs(points_to_interpolation, n):
    split_diffs = [(points_to_interpolation[i][1] if i < n+1 else 0)
                   for i in range(a_progression(a=1, b=n+1, n=n+1))]
    ind = n+1
    for i in range(n):
        offset = (n - 1 - i)
        for j in range(n-i):
            dy = split_diffs[ind - offset - 2] - split_diffs[ind - offset - 1]
            dx = points_to_interpolation[j][0] - points_to_interpolation[j+i+1][0]
            split_diffs[ind] = dy/dx
            ind += 1
    return split_diffs


def newton_interpolation(x, point_list, n):
    # Если вдруг точек очень мало
    if len(point_list) < n+1:
        return None

    point_list.sort()

    points_to_interpolation = get_points_to_interpolation(point_list=point_list, x=x, n=n)
    #print("Points to interpolation:")
    #print_points(points_to_interpolation)

    split_diffs = get_split_diffs(points_to_interpolation=points_to_interpolation, n=n)
    y = split_diffs[0]
    ind = n+1
    for i in range(1, n+1):
        add = split_diffs[ind]
        ind += n - i + 1
        for k in range(i):
            add *= (x - points_to_interpolation[k][0])
        y += add
    return y
