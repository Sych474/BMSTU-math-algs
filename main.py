from math import *
from baze_interpolation import *
from  multi_interp import *


def f(x):
    return sin(x)


def z(x, y):
    return x*x + y*y


def print_multi_table(table):
    print("|    x  |    y  |    z  |")
    for point in table:
        print("|{:7.3f}|{:7.3f}|{:7.3f}|".format(point[0], point[1], point[2]))


def print_multy_matr(table):
    table.sort()
    curr_x = table[0][0]
    for point in table:
        if point[0] == curr_x:
            print("{:4.1f}".format(point[2]), end=" ")
        else:
            curr_x = point[0]
            print()
            print("{:4.1f}".format(point[2]), end=" ")
    print()


def prepare_table(x_min, x_max, y_min, y_max, dx, dy, z):
    table = list()
    x = x_min
    while x <= x_max:
        y = y_min
        while y <= y_max:
            table.append((x, y, z(x, y)))
            y += dy
        x += dx
    return table


def prepair_matr(x_min, x_max, y_min, y_max, dx, dy, z):
    matr = list()
    x = x_min
    while x <= x_max:
        tmp = [x, list()]
        y = y_min
        while y <= y_max:
            tmp[1].append((y, z(x, y)))
            y += dy
        x += dx
        matr.append(tmp)
    return matr


def get_table():
    print("Input count of points: ")
    n = int(input())
    point_list = list()
    for i in range(n):
        point_list.append(tuple(map(float, input().split())))
    return point_list


def print_points(point_list):
    print("|    x  |    y  |")
    for point in point_list:
        print("|{:7.3f}|{:7.3f}|".format(point[0], point[1]))


def main():
    points = list()
    for x in range(-5, 6):
        points.append((x, f(x)))
    print("Points:")
    print_points(point_list=points)

    x = float(input("Input x: "))
    n = int(input("Input n: "))

    y = newton_interpolation(x=x, n=n, point_list=points)
    print("calculated: y({:.2f}) = {:7.3f}".format(x, y))
    print("real value: y({:.2f}) = {:7.3f}".format(x, f(x)))
    print("Relative error: {:6.3}%".format(((y - f(x))/f(x) * 100)))


def F1(x, y):
    return e**(x**3 - y) - (x**3) * (x**3 - 2*y - 2) - (y*y + 2*y + 2)


def F2(x, y):
    return e**(2*log(x) - y) + y * e**(-y) - (e**(x*x)) * (log(x*x + y))


def get_y(f, x, a, b, abs_eps):
    eps = abs((a-b)) * abs_eps
    y = (a+b) / 2
    while abs((a - b)) > eps:
        y = (a+b) / 2
        if f(x, y) * f(x, a) > 0:
            a = y
        else:
            b = y
    #print(f(x, y))
    return y


def get_zero(f1, f2, a, b, dx):
    points = list()
    x = a
    while x < b:
        points.append((get_y(f1, x, 0.1, 300, 10**-10) - get_y(f2, x, 0.1, 300, 10**-10), x))
        x += dx
    print_points(points)
    x = newton_interpolation(x=0, point_list=points, n=5)
    return x


x_min = 0
x_max = 20
y_min = 0
y_max = 20
dx = 2
dy = 2
matr = prepair_matr(x_min=x_min,x_max=x_max, y_min=y_min, y_max=y_max,dx=dx, dy=dy, z=z)
x = 1.222
y = 1.1345763
real_z = z(x, y)
calc_z = multy_interp(matr=matr, n_x=3, n_y=2, x=x, y=y)
print("calculated z: ", calc_z)
print("real z(x,y): ", real_z)
print("difference: ", real_z - calc_z)
print("error: {:5.2f}%".format(abs(calc_z - real_z)/calc_z*100))



#x = get_zero(F1, F2, 0.1, 2., 0.1)
#y = get_y(F1, x, -100, 100, 10**-7)
#print(F1(x, y))
#print(F2(x, y))
#print(F1(x, y) - F2(x, y))
#print("x: {:6.3f}\ny: {:6.3f}".format(x, y))

