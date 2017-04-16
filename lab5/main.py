from math import sqrt, pi, e


def gauss_integral(a, b, f, n):
    return 0


def ft(t):
    return e ** (-t*t/2)


def get_integral(x, n):
    return 1/sqrt(2*pi) * gauss_integral(0, x, ft, n)


def main():
    pass


if __name__ == '__main__':
    main()
