"""
interpolation functions
"""


"""
This function counts the different difference
@ x - table of x values
@ y - table of y values
"""


def difdif(x, y):
    if (len(y) != len(x)):
        print('Unappropriate x and y size in difdif.')
        return 0

    if len(x) < 2:
        print('difdif error')
        return 0

    if len(x) == 2:
        res = (y[0] - y[1]) / (x[0] - x[1])
        return res
    else:
        return (difdif(x[:-1], y[:-1]) - difdif(x[1:], y[1:])) / (x[0] - x[len(x) - 1])


"""
Finds the position for interpolation in list of x values
@ x - value
@ xt - list of values
"""


def find_pos(x, xt):
    i = 0
    while (x > xt[i] and i < len(xt) - 1):
        i += 1
    return i


"""
Make choice for interpolation
@ pos - start position
@ x - list of x values
@ y - list of y values
@ n - polynom degree
"""


def make_choice(pos, x, n):
    if n > len(x):
        print("Make_choice error")
        return 0, 0

    left, right = pos, pos
    r, l = n // 2, n // 2
    j = n % 2

    if left - l < 0:
        r = r - left + l
        l = 0

    if right + r >= len(x):
        l = l + right + r - len(x) + 1
        r = len(x) - 1

    left -= l
    right += r

    if j == 1:
        if left - 1 >= 0:
            left = left - 1
        else:
            right += 1

    return (int(left), int(right + 1))


"""
The function makes interpolation on y(x)
@ x - value
@ xt - table of x values
@ yt - table of y values
@ n - polynom degree
"""


def interpolate(x, xt, yt, n, flag=0):
    if len(xt) != len(yt):
        print("Incorrect input values.")
        return 0

    pos = find_pos(x, xt)
    l, r = make_choice(pos, xt, n)
    work_x, work_y = xt[l:r], yt[l:r]

    if flag:
        print('|', '{:^10}'.format('x'), '|', '{:^10}'.format('y'), '|')
        for i in range(len(work_x)):
            print('|', '{:^10.4g}'.format(work_x[i]),
                  '|', '{:^10.4g}'.format(work_y[i]), '|')

    cur = 0
    tmp = 1
    res = work_y[0]

    while cur < n:
        cur += 1
        tmp *= x - work_x[cur - 1]
        res += tmp * difdif(work_x[:cur + 1], work_y[:cur + 1])

    return res


def prepare_spline_table(x, y):
    n = len(x)
    ksi_array = [0 for i in range(n)]
    eta_array = [0 for i in range(n)]
    a = [0 for i in range(n)]
    b = [0 for i in range(n)]
    c = [0 for i in range(n)]
    d = [0 for i in range(n)]
    A = 0; B = 0; D = 0; F = 0; hi_next = 0; hi_prev = 0
    #Прогонка прямой шаг
    for i in range(1, n-1):
        hi_prev = x[i] - x[i-1]
        hi_next = x[i+1] - x[i]
        B = 2 * (hi_prev + hi_next)
        F = 6 * ((y[i+1]-y[i])/hi_next - (y[i]-y[i-1])/hi_prev)
        K = (B + hi_prev * ksi_array[i-1])
        ksi_array[i] = -hi_next/K
        eta_array[i] = (F - hi_prev * eta_array[i-1])/K


    # Костыли
    if (n-1 < 1):
        c[n-1] = (F - hi_prev*eta_array[n-2])/(B + hi_prev * ksi_array[n-2])
    # Прогонка обратный ход
    for i in range(n-2, 0, -1):
        c[i] = c[i+1] * ksi_array[i] + eta_array[i]

    for i in range(1, n):
        hi_curr = x[i] - x[i-1]
        a[i] = y[i]
        d[i] = (c[i] - c[i-1])/hi_curr
        b[i] = hi_curr * (2*c[i] + c[i-1]) / 6 + (y[i] - y[i-1])/hi_curr
    return a, b, c, d


def get_x_y(f, a, b, dx):
    x_arr = list()
    y_arr = list()
    x = a
    while x <= b:
        x_arr.append(x)
        y_arr.append(f(x))
        x += dx
    return x_arr, y_arr


def spline_interpolation(a, b, c, d, x_arr, x):
    n = len(x_arr)
    if x < x_arr[0]:
        ind = 0
    elif x > x_arr[n-1]:
        ind = n-1
    else:
        left = 0
        right = n-1
        while (left+1 < right):
            mid = (left + right) // 2
            if x < x_arr[mid]:
                right = mid
            else:
                left = mid
        ind = right
    dx = (x-x_arr[ind])
    y = a[ind] + b[ind]*dx + c[ind]*dx**2/2 + d[ind]*dx**3/6
    return y
