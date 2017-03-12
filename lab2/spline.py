from math import sin


def prepare_spline_table(x, y):
    n = len(x)
    ksi_array = [0 for i in range(n)]
    eta_array = [0 for i in range(n)]
    a = [0 for i in range(n)]
    b = [0 for i in range(n)]
    c = [0 for i in range(n)]
    d = [0 for i in range(n)]
    A = 0; B = 0; D = 0; F = 0; hi_next = 0; hi_prev = 0;
    for i in range(1, n-1):
        hi_prev = x[i] - x[i-1]
        hi_next = x[i+1] - x[i]
        B = 2 * (hi_prev + hi_next)
        F = 6 * ((y[i+1]-y[i])/hi_next - (y[i]-y[i-1])/hi_prev)
        K = (B + hi_prev * ksi_array[i-1])
        ksi_array[i] = -hi_next/K
        eta_array[i] = (F - hi_prev * eta_array[i-1])/K

    #Pn = 3 * ((x_y[n][1]-x_y[n-1][1])/hn - (x_y[n-1][1]-x_y[n-2][1])/hn_1)
    #Mn = hn_1
    #Kn = 2 * (hn + hn_1)
    #c[n] = (Pn - Mn * eta_array[n]) / (Kn + Mn * ksi_array[n])
    c[n-1] = (F - hi_prev*eta_array[n-2])/(B + hi_prev * ksi_array[n-2])
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


def spline_interpolation(a, b, c, d, x_arr,  x):
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


def f(x):
    return sin(4*x)


x, y = get_x_y(f=f, a=-5, b=5, dx=1)
a, b, c, d = prepare_spline_table(x=x, y=y)
print(a)
print(b)
print(c)
print(d)

x1 = 1.1
x2 = 1.2
x3 = 1.5
x4 = 2
y1 = spline_interpolation(a=a, b=b, c=c, d=d, x_arr=x, x=x1)
y2 = spline_interpolation(a=a, b=b, c=c, d=d, x_arr=x, x=x2)
y3 = spline_interpolation(a=a, b=b, c=c, d=d, x_arr=x, x=x3)
y4 = spline_interpolation(a=a, b=b, c=c, d=d, x_arr=x, x=x4)
print("x = ", x1, "y = ", y1)
print("x = ", x2, "y = ", y2)
print("x = ", x3, "y = ", y3)
print("x = ", x4, "y = ", y4)