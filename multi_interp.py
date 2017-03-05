import baze_interpolation


def get_lower_x_ind_to_interp(matr, n_x, x):
    x_ind = 0
    while x_ind < len(matr) and matr[x_ind][0] < x:
        x_ind += 1
    x_lower_ind = x_ind - n_x // 2 - n_x % 2  # если нечетное, то вниз берем больше.
    x_upper_ind = x_ind + n_x // 2
    if x_lower_ind < 0:
        x_upper_ind += abs(x_lower_ind)
        x_lower_ind = 0
    elif x_upper_ind >= len(matr):
        x_lower_ind -= x_upper_ind - (len(matr) - 1)
        x_upper_ind = len(matr) - 1
    return x_lower_ind


def multy_interp(matr, x, y, n_x, n_y):
    x_low = get_lower_x_ind_to_interp(matr=matr, x=x, n_x=n_x)
    x_z = list()
    for i in range(n_x+1):
        z_tmp = baze_interpolation.newton_interpolation(x=y, point_list=matr[x_low+i][1], n=n_y)
        x_z.append((matr[x_low+i][0], z_tmp))
    z = baze_interpolation.newton_interpolation(x=x, point_list=x_z, n=n_x)
    return z
