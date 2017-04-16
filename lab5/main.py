from math import sqrt, pi, e, cos

EPS = 10**-10


def P(n, x):
    if n == 0:
        return 1
    if n == 1:
        return x
    return (2*(n-1)+1)/((n-1)+1) * x * P(n-1, x) - (n-1)/((n-1)+1) * P(n-2, x)


def P_derivative(n, x):
    return n / (1 - x*x) * (P(n-1, x) - x*P(n, x))


def legendre_roots(n):
    roots = list()

    for i in range(1, n+1):
        x_old = cos(pi*(4*i - 1)/(4*n + 2))
        x_new = x_old - P(n=n, x=x_old)/P_derivative(n=n, x=x_old)

        while abs(x_new - x_old)/x_old >= EPS:
            x_old, x_new = x_new, x_new - P(n=n, x=x_new)/P_derivative(n=n, x=x_new)
        roots.append(x_new)
    return roots


def gauss_integral(a, b, f, n):
    roots = legendre_roots(n=n)
    return 0


def ft(t):
    return e ** (-t*t/2)


def get_integral(x, n):
    return 1/sqrt(2*pi) * gauss_integral(a=0, b=x, f=ft, n=n)


def main():
    pass


if __name__ == '__main__':
    main()
